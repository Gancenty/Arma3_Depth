import os
import json
import numpy as np
import open3d as o3d
from pcd_process import *

# -----------------------------------------------------------------------------------------------------------------------------#

# key_category = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\key_to_category.json"
# )
# object_info = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\object_info.json"
# )
# category_info_path = os.path.join(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info",
#     "category_info.json",
# )

# category_to_color = dict()
# for key, category in key_category.items():
#     assert key in object_info.keys()
#     color = object_info[key]["color"]
#     hex_color = object_info[key]["hex_color"]
#     if category not in category_to_color.keys():
#         category_info = dict()
#         category_info["color"] = color
#         category_info["hex_color"] = hex_color
#         category_info["object_name"] = [key]
#         category_to_color[category] = category_info
#     else:
#         object_name_list = category_to_color[category]["object_name"]
#         object_name_list.append(key)
#         category_to_color[category]["object_name"] = object_name_list

# save_ref_json_file(category_to_color, category_info_path)

# -----------------------------------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------------------------------#

# category_info = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\category_info.json"
# )

# def check_color_map(color_map: dict, believe_color=True):
#     hex_color_list = list()
#     for key, item in color_map.items():
#         color = item["color"]
#         hex_color = item["hex_color"]
#         if rgb_to_hex(color) != hex_color:
#             if believe_color:
#                 print(f"{key} hex color should be {rgb_to_hex(color)}")
#             else:
#                 print(f"{key} color should be {hex_to_rgb(hex_color)}")

#         if hex_color not in hex_color_list:
#             hex_color_list.append(hex_color)
#         else:
#             print(f"{hex_color} errer!")

# check_color_map(category_info)

# -----------------------------------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------------------------------#

# pcd_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Wiped\Building-0.1.ply"
# save_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Wiped\Building-0.1-Merged.ply"

# key_category = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\key_to_category.json"
# )
# category_info = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\category_info.json"
# )
# color_info = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\color_info.json"
# )
# object_info = load_ref_json_file(
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Object_Info\object_info.json"
# )

# no_need_filter_list = list()
# for key,info in object_info.items():
#     if key not in key_category.keys():
#         no_need_filter_list.append(key)
#         print(key)

# pcd = o3d.io.read_point_cloud(pcd_path)
# points = np.asarray(pcd.points)
# normals = np.asarray(pcd.normals)
# colors = np.asarray(pcd.colors)

# for i, item in enumerate((tqdm(colors, desc="Processing .ply files"))):
#     object_name = color_to_object(colors[i], color_info)
#     if object_name != False:
#         if object_name in no_need_filter_list:
#             # print(f"{object_name} dont need refine")
#             continue
#         else:
#             category = key_category[object_name]
#             color = category_info[category]["color"]
#             colors[i] = np.array(color) / 255.0

# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.normals = o3d.utility.Vector3dVector(normals)
# pcd.colors = o3d.utility.Vector3dVector(colors)
# o3d.io.write_point_cloud(save_path, pcd)

# -----------------------------------------------------------------------------------------------------------------------------#
