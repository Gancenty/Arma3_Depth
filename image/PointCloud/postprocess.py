import os
from tqdm import tqdm
import numpy as np
import open3d as o3d


def refine_point_cloud(points, voxel_size=0.01):
    points = points.remove_non_finite_points()
    points = points.remove_duplicated_points()
    points = points.voxel_down_sample(voxel_size)
    return points


def wipe_out_point_cloud(folder, x, y, width, height):
    folder_path = folder
    x_min = x
    y_min = y
    x_max = x + width
    y_max = y + height
    z_min = 0
    z_max = 500
    start_point = np.array([x_min, y_min, z_min])  # 替换为区域的起点坐标
    end_point = np.array([x_max, y_max, z_max])    # 替换为区域的终点坐标

    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]

    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        pcd = refine_point_cloud(pcd)

        points = np.asarray(pcd.points)
        normals = np.asarray(pcd.normals)

        in_box_mask = np.all((points >= start_point) & (points <= end_point), axis=1)
        filtered_points = points[in_box_mask]
        filtered_normals = normals[in_box_mask]

        filtered_pcd = o3d.geometry.PointCloud()
        filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
        filtered_pcd.normals = o3d.utility.Vector3dVector(filtered_normals)

        output_path = f"./Filted/{filename}"
        o3d.io.write_point_cloud(output_path, filtered_pcd)


def merge_point_cloud(folder):
    folder_path = folder
    total_pcd = o3d.geometry.PointCloud()
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    cnt = 0
    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        total_pcd = total_pcd + pcd
        if (cnt % 100) == 0:
            total_pcd = refine_point_cloud(total_pcd)
            print("refined")
        cnt += 1

    output_path = f"./Filted/total.ply"
    o3d.io.write_point_cloud(output_path, total_pcd)

def test_point_cloud(folder):
    folder_path = folder
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        arr = np.asarray(pcd.points)
        print(arr.shape)



work_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Arma3_Building\Arma3_PointCloud"

# test_point_cloud(r"E:\E_Disk_Files\Arma3_PointCloud\Arma3_Forest\Filted")
# wipe_out_point_cloud(work_dir, 8600, 18100, 100, 100)
merge_point_cloud("./Filted")
