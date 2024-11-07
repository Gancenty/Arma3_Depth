import open3d as o3d
import numpy as np

file_path = r"F:\Arma3_Building\Arma3_PointCloud\[8600-18100].ply"
pcd = o3d.io.read_point_cloud(file_path)
pcd = pcd.voxel_down_sample(voxel_size=0.05)
print(pcd)
o3d.visualization.draw_geometries([pcd])