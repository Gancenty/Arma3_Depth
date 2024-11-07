import open3d as o3d
import numpy as np
import os
from tqdm import tqdm

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

test_point_cloud(r"E:\E_Disk_Files\Arma3_PointCloud\Arma3_Forest\Filted")