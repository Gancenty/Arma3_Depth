import os
import zmq
import time
import logging
import threading
import numpy as np
import open3d as o3d


class Arma3_PointsCloud:
    def __init__(
        self,
        start_x=0,
        start_y=0,
        width=100,
        height=100,
        stride=5,
        store_path="./PointsCloud",
    ):
        self.received_cnt = 0
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.stride = stride
        self.grid_points = self.generate_grid((start_x, start_y), height, width, stride)
        # for i, j in enumerate(self.grid_points):
        #     print(i, j)
        self.zmq_sub_port = 5555
        self.zmq_pub_port = 5556
        self.communication_port = 5557

        self.is_finnished = False
        self.now_coord_index = 0
        self.data_lock = threading.Lock()
        self.store_path = store_path

        self.init_zmq()
        self.setup_logger()
        self.init_open3d()
        self.start_thread()

    def setup_logger(self, log_file="app.log", log_level=logging.INFO):
        logger = logging.getLogger("Logger")
        logger.setLevel(log_level)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        self.logger = logger

    def init_zmq(self):
        sub_context = zmq.Context()
        self.pcl_sub_socket = sub_context.socket(zmq.SUB)
        self.pcl_sub_socket.connect(f"tcp://localhost:{self.zmq_sub_port}")
        self.pcl_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        pub_context = zmq.Context()
        self.pcl_pub_socket = pub_context.socket(zmq.PUB)
        self.pcl_pub_socket.bind(f"tcp://127.0.0.1:{self.zmq_pub_port}")

        com_context = zmq.Context()
        self.com_socket = com_context.socket(zmq.SUB)
        self.com_socket.connect(f"tcp://localhost:{self.communication_port}")
        self.com_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def init_open3d(self):
        point_cloud = o3d.geometry.PointCloud()
        self.point_cloud = point_cloud

    def start_thread(self):
        time.sleep(1)
        self.threads = []
        self.threads.append(threading.Thread(target=self.parse_pointcloud, daemon=True))
        self.threads.append(threading.Thread(target=self.communication, daemon=True))
        for thread in self.threads:
            thread.start()

    def generate_grid(self, start_coord, height, width, stride):
        x_coords = np.arange(start_coord[0], start_coord[0] + width + stride, stride)
        y_coords = np.arange(start_coord[1], start_coord[1] + height + stride, stride)
        xx, yy = np.meshgrid(x_coords, y_coords)
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        return grid_points

    def parse_pointcloud(self):
        self.pcl_pub_socket.send_string(
            str(self.grid_points[self.now_coord_index].tolist())
        )
        while True:
            try:
                while True:
                    self.latest_msg = self.pcl_sub_socket.recv()

                    rec_data = np.frombuffer(self.latest_msg, dtype=np.float32)
                    rec_data = rec_data.reshape(-1, 6)
                    points = rec_data[:, :3]
                    normals = rec_data[:, 3:6]

                    if points.shape[0] == 0:
                        print("no points cloud")
                        continue

                    current_points = np.asarray(self.point_cloud.points)
                    current_normals = np.asarray(self.point_cloud.normals)

                    all_points = np.vstack((current_points, points))
                    all_normals = np.vstack((current_normals, normals))

                    self.point_cloud.points = o3d.utility.Vector3dVector(all_points)
                    self.point_cloud.normals = o3d.utility.Vector3dVector(all_normals)

                    with self.data_lock:
                        self.received_cnt += rec_data.shape[0]
            except zmq.Again:
                time.sleep(0.01)

    def communication(self):
        while True:
            try:
                while True:
                    data = self.com_socket.recv_string(zmq.NOBLOCK)
                    if data[0] == "Y":
                        with self.data_lock:
                            file_name = "[{0}-{1}].ply".format(
                                self.grid_points[self.now_coord_index][0],
                                self.grid_points[self.now_coord_index][1],
                            )
                            self.logger.info(
                                "Finished:%d,Rec:%d,Total:%s,File_name:%s"
                                % (
                                    self.now_coord_index + 1,
                                    self.received_cnt,
                                    data[1:],
                                    file_name,
                                )
                            )
                            path_name = os.path.join(self.store_path, file_name)
                            o3d.io.write_point_cloud(path_name, self.point_cloud)
                            self.point_cloud = o3d.geometry.PointCloud()
                            self.received_cnt = 0
                        if self.now_coord_index + 1 < len(self.grid_points):
                            self.now_coord_index += 1
                            self.pcl_pub_socket.send_string(
                                str(self.grid_points[self.now_coord_index].tolist())
                            )

            except zmq.Again:
                time.sleep(0.1)

if __name__ == "__main__":
    pcl = Arma3_PointsCloud(
        start_x=8450, start_y=18750, width=0, height=0, stride=5
    )
    try:
        while True:
            with pcl.data_lock:
                pcl.logger.info(
                    "Rec:%d,Now:%d,Total:%d"
                    % (pcl.received_cnt, pcl.now_coord_index + 1, len(pcl.grid_points))
                )
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting")
