import open3d as o3d
import numpy as np

# 加载点云文件
pcd = o3d.io.read_point_cloud(
    r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Wiped\Building-0.1.ply"
)  # 替换成你的文件路径
points = np.asarray(pcd.points)

print(points[:3])
# # 设置稀疏采样的步长，例如每隔100个点保留一个点
# # sampling_step = 50
# # pcd_downsampled = pcd.uniform_down_sample(sampling_step)

# # 设置点云显示的点大小
# vis = o3d.visualization.Visualizer()
# vis.create_window()

# # 添加点云
# vis.add_geometry(pcd)

# # 设置点大小
# opt = vis.get_render_option()
# opt.point_size = 7  # 这里设置点的大小为 5，你可以根据需要调整

# # 开始可视化
# vis.run()
# vis.destroy_window()

# # 定义观察点和方向
# view_point = np.array([8600, 18100, 182])  # 观察点的坐标，替换为你希望的值
# direction = np.array([1, 1, 0])  # 观察方向的单位向量

# # 定义视场角（FOV）以度为单位
# fov_angle = 45.0  # 例如 45 度，可以根据需求调整

# # 计算方向的单位向量
# direction = direction / np.linalg.norm(direction)
# pcd = pcd.remove_duplicated_points()
# # 将点云转换为numpy数组以便操作
# points = np.asarray(pcd.points)
# print(points.shape)
# # 计算每个点相对于观察点的向量
# vectors = points - view_point

# # 计算每个点与观察方向的夹角
# cos_angles = np.dot(vectors, direction) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(direction))

# # 将角度转为度
# angles = np.degrees(np.arccos(cos_angles))

# # 筛选满足FOV内的点
# mask = angles < fov_angle / 2
# visible_points = points[mask]

# # 将筛选后的点转换为点云对象
# visible_pcd = o3d.geometry.PointCloud()
# visible_pcd.points = o3d.utility.Vector3dVector(visible_points)

# 可视化

# o3d.visualization.draw_geometries([pcd])
