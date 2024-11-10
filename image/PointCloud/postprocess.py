import json
import logging
import os
import re
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
    input_path, output_path, x, y, width, height, reserved=5, rectify=False
):
    folder_path = input_path
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

            output_file = os.path.join(output_path, filename)
            o3d.io.write_point_cloud(output_file, filtered_pcd)
        else:
            output_file = os.path.join(output_path, filename)
            o3d.io.write_point_cloud(output_file, pcd)


def merge_point_cloud(input_path, output_path):
    folder_path = input_path
    total_pcd = o3d.geometry.PointCloud()
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    ply_files.sort()
    cnt = 0
    for index, filename in enumerate(tqdm(ply_files, desc="Processing .ply files")):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        total_pcd = total_pcd + pcd
        if (cnt % 100) == 0:
            total_pcd = refine_point_cloud(total_pcd)
            output_file_name = file_path = os.path.join(
                output_path, f"merged-{cnt}.ply"
            )
            o3d.io.write_point_cloud(output_file_name, total_pcd)
            print(f"Refined: Index:{index}-FileName:{filename}")
        cnt += 1
    total_pcd = refine_point_cloud(total_pcd)
    output_file_name = file_path = os.path.join(folder_path, f"merged.ply")
    o3d.io.write_point_cloud(output_file_name, total_pcd)


def test_point_cloud(input_path):
    folder_path = input_path
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        arr = np.asarray(pcd.points)
        print(arr.shape)


def voxel_point_cloud(input_file, output_file, voxel_size):
    points = o3d.io.read_point_cloud(input_file)
    points = points.voxel_down_sample(voxel_size)
    o3d.io.write_point_cloud(output_file, points)


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
            print("Color_Len:%d" % len(color_dict))
            return color_dict
    else:
        return None


def load_object_list(file_path, output_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            object_list = pickle.load(file)
            print("Object_Len:%d" % len(object_list))
            with open(output_path, "w") as out_file:
                for item in object_list:
                    out_file.write(f"{item}\n")
            return object_list
    else:
        return None


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def build_refer_json(color_dict, object_list, store_file_path):
    if color_dict is None or object_list is None:
        print("Failed to load color_dict or object_list")
        return
    ref_dict = {}
    for object_info, index in object_list:
        if index in color_dict:
            color = color_dict[index]
            normalize_color = [rgb / 255.0 for rgb in color]
            restore_color = [rgb * 255 for rgb in normalize_color]
            match = re.search(r"\b\w+\.p3d\b", object_info)
            if match:
                object_name = match.group(0).split(".")[0]
            else:
                object_name = object_info

            info_dict = {}
            info_dict["color"] = color
            info_dict["normalize_color"] = normalize_color
            info_dict["restore_color"] = restore_color
            info_dict["index"] = index
            info_dict["object"] = object_info
            info_dict["object_name"] = object_name
            ref_dict[rgb_to_hex(color)] = info_dict
        else:
            print(f"{object_info} and {index} is not in color_dict")
    with open(store_file_path, "w") as file:
        json.dump(ref_dict, file, sort_keys=True, indent=4)


def points_color_merge(file_name):
    pass


def color_to_object(points_color, ref_dict: dict):
    restore_color = [int(rgb * 255) for rgb in points_color]
    hex_color_str = rgb_to_hex(restore_color)
    if hex_color_str in ref_dict.keys():
        return ref_dict[hex_color_str]["object_name"]
    else:
        print("Failed:", hex_color_str)
        return False


def open_ply_files(file_name):
    pcd = o3d.io.read_point_cloud(file_name)
    return pcd


def setup_logger(log_file="postprocess.log", log_level=logging.INFO):
    logger = logging.getLogger("Logger")
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def load_ref_json_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            color_dict = json.load(file)
            print("Color_Len:%d" % len(color_dict))
            return color_dict
    else:
        return None


def test_color_mapping(input_path, ref_json):
    folder_path = input_path
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    fail_cnt = 0
    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        color = np.asarray(pcd.colors)
        for i in range(len(color)):
            ans = color_to_object(color[i], ref_json)
            if ans == False:
                fail_cnt += 1
        if fail_cnt:
            logger.error(f"{filename} Failed_cnt:{fail_cnt}")
        else:
            logger.info(f"{filename} Failed_cnt:{fail_cnt}")


def process_object_list(file_path, output_path):
    unique_object = dict()
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            object_list = pickle.load(file)
            print("Object_Len:%d" % len(object_list))
            for item, index in object_list:
                match = re.search(r"\b\w+\.p3d\b", item)
                if match:
                    object_name = match.group(0).split(".")[0]
                    if object_name not in unique_object.keys():
                        unique_object[object_name] = index
                else:
                    unique_object[item] = index
        with open(output_path, "w") as out_file:
            json.dump(unique_object, out_file, sort_keys=True, indent=4)
        return unique_object


def refine_colored_point_cloud(
    input_path, output_path, color_dict, color_info, unique_object
):
    folder_path = input_path
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    for index, filename in enumerate(tqdm(ply_files, desc="Processing .ply files")):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        color = np.asarray(pcd.colors)
        for i, item in enumerate((tqdm(color, desc="Processing .ply files"))):
            object_name = color_to_object(color[i], color_info)
            if object_name != False:
                color_index = unique_object[object_name]
                color[i] = np.array(color_dict[str(color_index)]) / 255.0
            else:
                print("ERROR!")
        pcd.colors = o3d.utility.Vector3dVector(color)
        file_path = os.path.join(output_path, filename)
        o3d.io.write_point_cloud(file_path, pcd)


logger = setup_logger()

work_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored"
output_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Filted"

in_path_name = r"D:\Gancenty\Desktop"
in_file_name = "total-0.1.ply"

out_path_name = ""
out_file_name = ""

color_info_json = load_ref_json_file("color_info.json")
color_json = load_ref_json_file("color_dict.json")
object_json = load_ref_json_file("unique_object_json.json")

refine_colored_point_cloud(
    r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored",
    r"Filted/",
    color_json,
    color_info_json,
    object_json,
)
# test_color_mapping(work_dir, ref_json)

# process_object_list("object_list.pkl", "unique_object_json.json")

# color_dict = load_color_dict("color_dict.json")
# object_list = load_object_list("object_list.pkl","1.txt")
# build_refer_json(color_dict=color_dict, object_list=object_list, store_file_path="./color_info.json")

# merge_two_point_cloud_file(r"F:\Arma3\PointsCloud\Arma3_Forest\1\PointsCloud",r"F:\Arma3\PointsCloud\Arma3_Forest\1\Add")
# wipe_out_height(path_name, file_name, 0, 250)
# voxel_point_cloud(path_name, file_name, 0.1)
# test_point_cloud(r"./Filted")
# wipe_out_point_cloud(work_dir, output_dir, 8450, 18750, 100, 100, rectify=False)
# merge_point_cloud("./Filted")
