# import open3d as o3d
# import numpy as np
# import cv2
# import time

# # Load the point cloud file
# pcd = o3d.io.read_point_cloud("Filted\[8500-18200].ply")

# # Initialize the Open3D visualizer
# vis = o3d.visualization.Visualizer()
# vis.create_window()
# vis.add_geometry(pcd)

# # Run a loop to update the depth map as the camera changes
# try:
#     while True:
#         # Capture the depth image from the current camera view
#         depth = vis.capture_depth_float_buffer(True)
#         depth_image = np.asarray(depth)

#         # Normalize depth image for display with OpenCV
#         depth_normalized = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

#         # Display the depth map using OpenCV
#         cv2.imshow("Depth Map from Point Cloud", depth_normalized)

#         # Check for 'q' key press to exit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#         # Allow Open3D to update the visualization and handle user inputs
#         vis.poll_events()
#         vis.update_renderer()

# except KeyboardInterrupt:
#     print("Closing visualization...")

# finally:
#     # Clean up Open3D and OpenCV windows
#     vis.destroy_window()
#     cv2.destroyAllWindows()

import open3d as o3d
import numpy as np
import random

# 加载点云
pcd = o3d.io.read_point_cloud(r"C:\Users\Miracle\Desktop\[8500-18200].ply")

# 设置体素大小并进行体素化
voxel_size = 0.5  # 设置适当的体素大小
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)

# 创建字典存储每个体素的颜色信息
voxel_colors = {}
voxel_list = voxel_grid.get_voxels()
# 遍历点云中的每个点
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)
for point, color in zip(points, colors):
    # 获取该点的体素坐标
    voxel_coord = voxel_grid.get_voxel(point)
    key = str(voxel_coord.tolist())
    # 将颜色信息存入字典，以体素坐标为键
    if key not in voxel_colors:
        voxel_colors[key] = []
    voxel_colors[key].append(color)

# 随机选择体素内的一个点的颜色
for voxel_coord, color_list in voxel_colors.items():
    key = str(voxel_coord)
    voxel_colors[key] = random.choice(color_list)

# 将颜色应用到体素网格
voxel_grid.color = o3d.utility.Vector3dVector(
    [voxel_colors[str(voxel.grid_index.tolist())] for voxel in voxel_grid.get_voxels()]
)

# 可视化
o3d.visualization.draw([voxel_grid])
