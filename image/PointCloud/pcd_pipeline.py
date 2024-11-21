from pcd_process import *
import os
import open3d as o3d
import shutil


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# *********************************************Merge Same Points Objects in Folder to Another*********************************************************


# def safe_copy(src, dst):
#     # 检查源文件和目标文件是否相同
#     if os.path.abspath(src) == os.path.abspath(dst):
#         print(f"源文件和目标文件相同：{src}")
#         return

#     shutil.copy(src, dst)
#     print(f"文件已复制到: {dst}")


# def merge_class_point_clouds(folder1, folder2, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     files1 = set(os.listdir(folder1))
#     files2 = set(os.listdir(folder2))

#     common_files = files1 & files2
#     unique_files1 = files1 - files2
#     unique_files2 = files2 - files1
#     for filename in common_files:
#         file1_path = os.path.join(folder1, filename)
#         file2_path = os.path.join(folder2, filename)
#         output_path = os.path.join(output_folder, filename)

#         try:
#             pcd1 = o3d.io.read_point_cloud(file1_path)
#             pcd2 = o3d.io.read_point_cloud(file2_path)

#             combined_pcd = pcd1 + pcd2
#             combined_pcd = combined_pcd.voxel_down_sample(0.1)
#             o3d.io.write_point_cloud(output_path, combined_pcd)
#             print(f"合并文件: {filename} -> {output_path}")
#         except Exception as e:
#             print(f"无法处理文件: {filename}, 错误: {e}")

#     for filename in unique_files1:
#         safe_copy(
#             os.path.join(folder1, filename), os.path.join(output_folder, filename)
#         )
#         print(f"复制文件: {filename} -> {output_folder}")

#     for filename in unique_files2:
#         safe_copy(
#             os.path.join(folder2, filename), os.path.join(output_folder, filename)
#         )
#         print(f"复制文件: {filename} -> {output_folder}")

#     print("处理完成！")


# folder1 = "/home/wangxy/lga/forest/class"  # 第一个文件夹路径
# folder2 = "/home/wangxy/lga/forest/class-7"  # 第二个文件夹路径
# output_folder = "/home/wangxy/lga/forest/class"  # 输出文件夹路径

# merge_class_point_clouds(folder1, folder2, output_folder)
# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# *********************************************Change Points Cloud Color in Folder to Another*********************************************************

# pcd_input_path = r"/home/wangxy/lga/Forest-7/Filtered/class"
# pcd_output_path = r"/home/wangxy/lga/forest/class-7"
# origin_color_info_path = r"/home/wangxy/lga/Forest-7/Object_Info/color_info.json"
# new_object_info_path = r"/home/wangxy/lga/forest/Object_Info/object_info.json"

# ply_files = [
#     filename for filename in os.listdir(pcd_input_path) if filename.endswith(".ply")
# ]

# for filename in tqdm(ply_files, desc="Processing .ply files"):
#     in_file_path = os.path.join(pcd_input_path, filename)
#     out_file_path = os.path.join(pcd_output_path, filename)
#     change_points_cloud_color(
#         in_file_path, out_file_path, origin_color_info_path, new_object_info_path
#     )
# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# ************************************First to Use to merge same object and remove unused  points*****************************************************

# object_info_input_path = r"/home/wangxy/lga/Forest-7/Object_Info"
# object_info_output_path = r"/home/wangxy/lga/Forest-7/Object_Info"
# input_dir = r"/home/wangxy/lga/Forest-7/Forest"
# output_dir = r"/home/wangxy/lga/Forest-7/Filtered"
# process_pipeline(
#     object_info_input_path,
#     object_info_output_path,
#     input_dir,
#     output_dir,
#     need_refine_points_cloud=True,
# )

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# *******************************************Merge all points cloud file to a entire file*************************************************************

input_file_path = r"/home/wangxy/lga/forest/class"
output_file_path = r"/home/wangxy/lga/forest"
merge_point_cloud(input_file_path, output_file_path)

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# ***********************************************Used to Reduce points cloud size*********************************************************************

# in_file_name = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Building-2-Filted.ply"
# )
# out_path_name = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Building-2-0.1.ply"
# )
# color_info_path = (
#     r"/Users/guoan/Documents/GitHub/Arma3_Depth/Arma3_Forest/color_info.json"
# )
# color_info = load_ref_json_file(color_info_path)
# voxel_point_cloud(in_file_name, out_path_name, color_info, 0.1)

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# ************************************Used to remove unused point in points cloud (animals, flying)***************************************************

# in_file_name = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Building-2.ply"
# )
# out_file_name = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Building-2-Filted.ply"
# )
# color_info_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Object_Info\color_info.json"
# unique_object_json_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Object_Info\unique_object_json.json"
# unique_object_json = load_ref_json_file(unique_object_json_path)
# color_info_json = load_ref_json_file(color_info_path)
# unused_list = get_unused_object_list(unique_object_json)
# remove_unused_object(in_file_name, out_file_name, color_info_json, unused_list)

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# *********************************************Used to merged two points cloud************************************************************************

# base_path = r"/home/wangxy/lga/forest/Object_Info"
# add_path = r"/home/wangxy/lga/Forest-7/Object_Info"
# output_path = r"/home/wangxy/lga/forest/Object_Info"
# merge_two_object_info(base_path, add_path, output_path)

# # only convert the color of points cloud file in add_path to desired color info file
# pcd_input_path = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3\Building-3-Filted.ply"
# )
# pcd_output_path = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\1-2\Building-3-Filted.ply"
# )
# origin_color_info_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3\Object_Info\color_info.json"
# new_object_info_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\1-2\Object_Info\object_info.json"
# change_points_cloud_color(
#     pcd_input_path, pcd_output_path, origin_color_info_path, new_object_info_path
# )

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# *********************************************Rectify points cloud to cut unneccssary boundary*******************************************************

# input_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3"
# output_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3"
# init_x_coord = 8500
# init_y_coord = 18100
# height = 300
# width = 300
# wipe_out_point_cloud(input_path, output_path, init_x_coord, init_y_coord, width, height)

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#
