import subprocess
import time
import numpy as np
import zmq

pcl_pub_port = 5555
pcl_sub_port = 5556
com_port = 5557

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://127.0.0.1:{pcl_pub_port}")

context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.connect(f"tcp://localhost:{pcl_sub_port}")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

context = zmq.Context()
com_socket = context.socket(zmq.PUB)
com_socket.bind(f"tcp://127.0.0.1:{com_port}")

def send_message(message):
    """
    ["image.send_message", [message]] call py3_fnc_callExtension;
    """
    point_cloud_data = np.array(message, dtype=np.float32)
    binary_data = point_cloud_data.tobytes()
    pub_socket.send(binary_data)


def read_message():
    """
    ["image.read_message", []] call py3_fnc_callExtension;
    """
    try:
        message = sub_socket.recv_string(zmq.NOBLOCK)
        return ["Y",eval(message)]
    except zmq.Again as e:
        return ["N",[0, 0]]

def send_com_message(message):
    """
    ["image.send_message", [message]] call py3_fnc_callExtension;
    """
    com_socket.send_string(message)