import json
import os
import pickle
from tqdm import tqdm
import numpy as np
import open3d as o3d


def refine_point_cloud(points, voxel_size=0.01):
    points = points.remove_non_finite_points()
    points = points.remove_duplicated_points()
    points = points.voxel_down_sample(voxel_size)
    return points


def wipe_out_point_cloud(
    input_folder, output_folder, x, y, width, height, reserved=5, rectify=False
):
    folder_path = input_folder
    x_min = x - reserved
    y_min = y - reserved
    x_max = x + width + reserved * 2
    y_max = y + height + reserved * 2
    z_min = 0
    z_max = 400
    start_point = np.array([x_min, y_min, z_min])  # 替换为区域的起点坐标
    end_point = np.array([x_max, y_max, z_max])  # 替换为区域的终点坐标

    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]

    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        pcd = refine_point_cloud(pcd)

        if rectify:
            points = np.asarray(pcd.points)
            normals = np.asarray(pcd.normals)
            in_box_mask = np.all(
                (points >= start_point) & (points <= end_point), axis=1
            )
            filtered_points = points[in_box_mask]
            filtered_normals = normals[in_box_mask]

            filtered_pcd = o3d.geometry.PointCloud()
            filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
            filtered_pcd.normals = o3d.utility.Vector3dVector(filtered_normals)

            output_path = os.path.join(output_folder, filename)
            o3d.io.write_point_cloud(output_path, filtered_pcd)
        else:
            output_path = os.path.join(output_folder, filename)
            o3d.io.write_point_cloud(output_path, pcd)


def merge_all_point_cloud(folder):
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


def voxel_point_cloud(path, filename, voxel_size):
    file_path = os.path.join(path, filename)
    output_path = os.path.join(path, "total-" + str(voxel_size) + ".ply")
    points = o3d.io.read_point_cloud(file_path)
    points = points.voxel_down_sample(voxel_size)
    o3d.io.write_point_cloud(output_path, points)


def wipe_out_height(path_name, file_name, z_min, z_max):
    file_path = os.path.join(path_name, file_name)
    pcd = o3d.io.read_point_cloud(file_path)

    points = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    colors = np.asarray(pcd.colors)

    in_box_mask = (points[:, 2] <= z_max) & (points[:, 2] >= z_min)

    filtered_points = points[in_box_mask]
    filtered_normals = normals[in_box_mask]
    filtered_colors = colors[in_box_mask]

    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_pcd.normals = o3d.utility.Vector3dVector(filtered_normals)
    filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

    output_path = f"./Filted/{file_name}"
    o3d.io.write_point_cloud(output_path, filtered_pcd)


def merge_two_point_cloud_file(folder1, folder2):
    ply_files1 = [
        filename for filename in os.listdir(folder1) if filename.endswith(".ply")
    ]
    ply_files2 = [
        filename for filename in os.listdir(folder2) if filename.endswith(".ply")
    ]

    for filename in tqdm(ply_files1, desc="Processing .ply files"):
        if filename not in ply_files2:
            continue
        file_path1 = os.path.join(folder1, filename)
        file_path2 = os.path.join(folder2, filename)

        total_pcd = o3d.geometry.PointCloud()
        pcd1 = o3d.io.read_point_cloud(file_path1)
        pcd2 = o3d.io.read_point_cloud(file_path2)
        total_pcd = pcd1 + pcd2
        output_path = f"./1/{filename}"
        o3d.io.write_point_cloud(output_path, total_pcd)


def load_color_dict(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            color_dict = json.load(file)
            color_dict = {int(k): v for k, v in color_dict.items()}
            print("Color_Len:%d"%len(color_dict))
            return color_dict
    else:
        return None


def load_object_list(file_path, output_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            object_list = pickle.load(file)
            print("Object_Len:%d"%len(object_list))
            with open(output_path, "w") as out_file:
                for item in object_list:
                    out_file.write(f"{item}\n")
            return object_list
    else:
        return None

def rgb_to_hex(rgb):
        return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])

def build_refer_dict(color_dict, object_list, store_file_path):
    if color_dict is None or object_list is None:
        print("Failed to load color_dict or object_list")
        return
    ref_dict = {}
    for object, index in object_list:
        if index in color_dict:
            color = color_dict[index]
            normalize_color = [rgb/255.0 for rgb in color]
            restore_color = [rgb*255 for rgb in normalize_color]
            info_dict = {}
            info_dict["color"] = color
            info_dict["normalize_color"] = normalize_color
            info_dict["restore_color"] = restore_color
            info_dict["index"] = index
            info_dict["object"] = object
            ref_dict[rgb_to_hex(color)] = info_dict
        else:
            print(f"{object} and {index} is not in color_dict")
    with open(store_file_path,"w") as file:
        json.dump(ref_dict, file, sort_keys=True, indent=4)

def points_color_merge(file_name):
    pass

def color_to_object(points_color, ref_dict: dict):
    restore_color = [int(rgb*255) for rgb in points_color]
    hex_color_str = rgb_to_hex(restore_color)
    if hex_color_str in ref_dict.keys():
        print(ref_dict[hex_color_str]["object"])

def open_ply_files(file_name):
    pcd = o3d.io.read_point_cloud(file_name)
    return pcd

def load_json_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            color_dict = json.load(file)
            print("Color_Len:%d"%len(color_dict))
            return color_dict
    else:
        return None

work_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored"
output_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Filted"

path_name = r"D:\Gancenty\Desktop"
file_name = "total-0.1.ply"

ref_json = load_json_file("./ref.json")
pcd = open_ply_files(r"D:\Gancenty\Desktop\[8800-18210].ply")
color = np.asarray(pcd.colors)
for i in range(10):
    print(color_to_object(color[i],ref_json))

# color_dict = load_color_dict("color_dict.json")
# object_list = load_object_list("object_list.pkl","1.txt")
# build_refer_dict(color_dict=color_dict, object_list=object_list, store_file_path="./ref.json")

# merge_two_point_cloud_file(r"F:\Arma3\PointsCloud\Arma3_Forest\1\PointsCloud",r"F:\Arma3\PointsCloud\Arma3_Forest\1\Add")
# wipe_out_height(path_name, file_name, 0, 250)
# voxel_point_cloud(path_name, file_name, 0.1)
# test_point_cloud(r"./Filted")
# wipe_out_point_cloud(work_dir, output_dir, 8450, 18750, 100, 100, rectify=False)
# merge_point_cloud("./Filted")
