import json
import logging
import os
import random
import re
import pickle
from tqdm import tqdm
import numpy as np
import open3d as o3d
import colorama

colorama.init(autoreset=True)


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


def refine_point_cloud(points, voxel_size=0.01):
    points = points.remove_non_finite_points()
    points = points.remove_duplicated_points()
    return points


def voxel_down_sample(points, voxel_size):
    points = points.voxel_down_sample(voxel_size)
    return points


def wipe_out_point_cloud(
    input_path, output_path, x, y, width, height, reserved=5, rectify=False
):
    folder_path = input_path
    x_min = x - reserved
    y_min = y - reserved
    x_max = x + width + reserved
    y_max = y + height + reserved
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
            colors = np.asarray(pcd.colors)
            in_box_mask = np.all(
                (points >= start_point) & (points <= end_point), axis=1
            )
            filtered_points = points[in_box_mask]
            filtered_normals = normals[in_box_mask]
            filtered_colors = colors[in_box_mask]

            filtered_pcd = o3d.geometry.PointCloud()
            filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
            filtered_pcd.normals = o3d.utility.Vector3dVector(filtered_normals)
            filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

            output_file = os.path.join(output_path, filename)
            o3d.io.write_point_cloud(output_file, filtered_pcd)
        else:
            output_file = os.path.join(output_path, filename)
            o3d.io.write_point_cloud(output_file, pcd)


def merge_point_cloud(input_path, output_path, need_refine=True):
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
        if (cnt % 100) == 0 and (cnt != 0):
            if need_refine:
                total_pcd = refine_point_cloud(total_pcd)
            output_file_name = os.path.join(output_path, f"merged-{cnt}.ply")
            o3d.io.write_point_cloud(output_file_name, total_pcd)
            print(f"Refined: Index:{index}-FileName:{filename}")
        cnt += 1
    if need_refine:
        total_pcd = refine_point_cloud(total_pcd)
    output_file_name = os.path.join(output_path, f"merged.ply")
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


def wipe_out_height(path_name, file_name, output_file, z_min, z_max):
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

    o3d.io.write_point_cloud(output_file, filtered_pcd)


def merge_two_point_cloud_file(folder1, folder2, output_path, voxel_size=0.1):
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
        total_pcd = total_pcd.voxel_down_sample(voxel_size)
        file_path = os.path.join(output_path, filename)
        o3d.io.write_point_cloud(file_path, total_pcd)


def load_color_dict(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            color_dict = json.load(file)
            color_dict = {int(k): v for k, v in color_dict.items()}
            print(
                f"{colorama.Fore.GREEN}Color_dict {colorama.Fore.RESET}{file_path}: {colorama.Fore.GREEN}{len(color_dict)}"
            )
            return color_dict
    else:
        return None


def load_object_list(file_path: str, output_path=None):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            object_list = pickle.load(file)
            print(
                f"{colorama.Fore.BLUE}Object_list {colorama.Fore.RESET}{file_path}: {colorama.Fore.BLUE}{len(object_list)}"
            )
            if output_path is None:
                return object_list
            object_list_dict = {}
            for name, index in object_list:
                object_list_dict[name] = index
            with open(output_path, "w") as file:
                json.dump(object_list_dict, file, sort_keys=True, indent=4)
            return object_list
    else:
        return None


def load_ref_json_file(file_name):
    """Loading a json file as dict()

    Args:
        file_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            color_dict = json.load(file)
            len_color_dict = len(color_dict)
            print(
                f"{colorama.Fore.YELLOW}Load Json {colorama.Fore.RESET}{file_name}: {colorama.Fore.YELLOW}{len_color_dict}"
            )
            return color_dict
    else:
        return None

def save_ref_json_file(dict_object, file_path):
    with open(file_path, "w") as out_file:
        json.dump(dict_object, out_file, sort_keys=True, indent=4)

def rgb_to_hex(rgb):
    """Used to covert rgb[0-255] the hex value

    Args:
        rgb (_type_): _description_

    Returns:
        _type_: _description_
    """
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])

def hex_to_rgb(hex):
    """Used to covert rgb[0-255] the hex value

    Args:
        rgb (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [int(hex[i:i+2], 16) for i in (1, 3, 5)]


def color_to_object(normalized_points_color, color_info_dict: dict):
    restore_color = [int(rgb * 255) for rgb in normalized_points_color]
    hex_color_str = rgb_to_hex(restore_color)
    if hex_color_str in color_info_dict.keys():
        return color_info_dict[hex_color_str]["object_name"]
    else:
        raise ValueError(f"Error {hex_color_str}")


def build_color_info_json(color_dict: dict, object_list: list, store_file_path: str):
    """Process the file generated by the main.py, \n

    which `color_dict` contains the index to rgb color[0-255]\n
    `object_list` contains the pairs of arma3 object name and\n
    the index

    Args:
        color_dict (_type_): _description_
        object_list (_type_): _description_
        store_file_path (_type_): _description_
    """
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
            hex_color_str = rgb_to_hex(color)
            info_dict = {}
            info_dict["color"] = color
            info_dict["normalize_color"] = normalize_color
            info_dict["restore_color"] = restore_color
            info_dict["hex_color"] = hex_color_str
            info_dict["index"] = index
            info_dict["object"] = object_info
            info_dict["object_name"] = object_name
            ref_dict[hex_color_str] = info_dict
        else:
            print(f"{object_info} and {index} is not in color_dict")
    print(
        f"{colorama.Fore.YELLOW}Color_info {colorama.Fore.RESET}{store_file_path}: {colorama.Fore.YELLOW}{len(ref_dict)}"
    )
    with open(store_file_path, "w") as file:
        json.dump(ref_dict, file, sort_keys=True, indent=4)


def build_unique_object_json(object_list_file_path, output_path):
    """According the description of arma3 object name, \n

    choose a shortest name and as a key to dict(), merge \n
    the same description about object

    Args:
        file_path (_type_): _description_
        output_path (_type_): _description_

    Returns:
        _type_: _description_····
    """
    unique_object = dict()
    if os.path.exists(object_list_file_path):
        with open(object_list_file_path, "rb") as file:
            object_list = pickle.load(file)
            for item, index in object_list:
                match = re.search(r"\b\w+\.p3d\b", item)
                if match:
                    object_name = match.group(0).split(".")[0]
                    if object_name not in unique_object.keys():
                        unique_object[object_name] = index
                else:
                    unique_object[item] = index
        print(
            f"{colorama.Fore.RED}Unique_object {colorama.Fore.RESET}{output_path}: {colorama.Fore.RED}{len(unique_object)}"
        )
        with open(output_path, "w") as out_file:
            json.dump(unique_object, out_file, sort_keys=True, indent=4)
        return unique_object


def build_object_info_json(
    unique_object: dict, color_dict: dict, color_info: dict, output_path: str
):
    """generate object_info.json as function to color_info.json\n

    the key is the short object name

    Args:
        unique_object (dict): _description_
        color_dict (dict): _description_
        color_info (dict): _description_
        output_path (str): _description_

    Returns:
        _type_: _description_
    """
    objects_info = {}
    for object_name, index in unique_object.items():
        info = {}
        hex_color_str = rgb_to_hex(color_dict[str(index)])
        info = color_info[hex_color_str]
        info["hex_color"] = hex_color_str
        objects_info[object_name] = info
    print(
        f"{colorama.Fore.GREEN}Objects_info {colorama.Fore.RESET}{output_path}: {colorama.Fore.GREEN}{len(objects_info)}"
    )
    with open(output_path, "w") as out_file:
        json.dump(objects_info, out_file, sort_keys=True, indent=4)
    return objects_info


def test_color_mapping(input_path, color_info_dict: dict):
    """Test the color of the `.ply` files in the folder that\n

    can be recognized as a object in `ref_json`

    Args:
        input_path (_type_): _description_
        ref_json (_type_): _description_
    """
    folder_path = input_path
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    fail_cnt = 0
    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        color = np.asarray(pcd.colors)
        loop = tqdm(range(len(color)), desc="Processing .ply files")
        for i in loop:
            ans = color_to_object(color[i], color_info_dict)
            if ans == False:
                fail_cnt += 1
            loop.set_description(f"Fail_cnt:{fail_cnt}")

        if fail_cnt:
            logger.error(f"{filename} Failed_cnt:{fail_cnt}")
        else:
            logger.info(f"{filename} Failed_cnt:{fail_cnt}")


def get_unused_object_list(unique_object: dict):
    """Continue with the `process_object_list`,\n

    add more constraint to reduce the object count

    Args:
        file_name (_type_): _description_
    """
    unused_list = []
    for i in unique_object.keys():
        if i[:5] == "Agent":
            unused_list.append(i)
    if "kestrel_f" in unique_object:
        unused_list.append("kestrel_f")
    return unused_list


def refine_colored_point_cloud(
    input_path: str,
    output_path: str,
    color_dict: dict,
    color_info: dict,
    unique_object: dict,
    voxel_size=0.1,
):
    """Used to merge the closed description in arma3 object name,\n

    according the `color_info` to find the short description of arma3 object name,\n
    and then get the index of the object name in `unique_object`, and choose \n
    a color according the `color_dict`

    Args:
        input_path (_type_): _description_
        output_path (_type_): _description_
        color_dict (_type_): _description_
        color_info (_type_): _description_
        unique_object (_type_): _description_
    """
    folder_path = input_path
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]
    unused_list = get_unused_object_list(unique_object)
    for index, filename in enumerate(tqdm(ply_files, desc="Processing .ply files")):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        points = np.asarray(pcd.points)
        normals = np.asarray(pcd.normals)
        colors = np.asarray(pcd.colors)
        mask = np.ones(len(colors), dtype=bool)
        object_to_pcd = {}
        for i, item in enumerate((tqdm(colors, desc="Processing .ply files"))):
            object_name = color_to_object(colors[i], color_info)
            if object_name != False:
                if object_name in unused_list:
                    mask[i] = False
                    continue
                color_index = unique_object[object_name]
                colors[i] = np.array(color_dict[str(color_index)]) / 255.0

                point_array = points[i]
                normal_array = normals[i]
                color_array = colors[i]

                if object_name not in object_to_pcd.keys():
                    object_to_pcd[object_name] = [
                        [point_array],
                        [normal_array],
                        [color_array],
                    ]
                else:
                    object_to_pcd[object_name][0].append(point_array)
                    object_to_pcd[object_name][1].append(normal_array)
                    object_to_pcd[object_name][2].append(color_array)

            else:
                print("x" * 20 + "ERROR!" + "x" * 20)

        for object_name, array in object_to_pcd.items():
            filtered_pcd = o3d.geometry.PointCloud()
            filtered_pcd.points = o3d.utility.Vector3dVector(np.vstack(array[0]))
            filtered_pcd.normals = o3d.utility.Vector3dVector(np.vstack(array[1]))
            filtered_pcd.colors = o3d.utility.Vector3dVector(np.vstack(array[2]))

            file_root = os.path.join(output_path, "class")
            if not os.path.exists(file_root):
                os.mkdir(file_root)
            if object_name != "<NULL-object>":
                file_path = os.path.join(file_root, object_name + ".ply")
            else:
                file_path = os.path.join(file_root, "NULL.ply")
            if os.path.isfile(file_path):
                origin_pcd = o3d.io.read_point_cloud(file_path)
                filtered_pcd = filtered_pcd + origin_pcd

            filtered_pcd = filtered_pcd.voxel_down_sample(voxel_size)
            o3d.io.write_point_cloud(file_path, filtered_pcd)
            del filtered_pcd

        points = points[mask]
        normals = normals[mask]
        colors = colors[mask]

        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.normals = o3d.utility.Vector3dVector(normals)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        file_path = os.path.join(output_path, filename)
        o3d.io.write_point_cloud(file_path, pcd)


def remove_unused_object(
    file_path: str, output_path: str, color_info: dict, unused_object_list: list
):
    """Remove unused object in unused_object_list such as animals, \n

    usually end with `agent` or `kestrel_f`

    Args:
        file_path (str): _description_
        output_path (str): _description_
        color_info (dict): _description_
        unused_object_list (list): _description_
    """
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    colors = np.asarray(pcd.colors)
    mask = np.ones(len(colors), dtype=bool)
    for i, color in enumerate(tqdm(colors, desc="Processing .ply files")):
        object_name = color_to_object(color, color_info)
        assert object_name != False, f"color_to_object error, object name:{object_name}"
        if object_name != False:
            if object_name in unused_object_list:
                mask[i] = False  # 标记需要删除的点
    points = points[mask]
    normals = normals[mask]
    colors = colors[mask]

    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.normals = o3d.utility.Vector3dVector(normals)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud(output_path, pcd)


def get_object_above_height(file_path, color_info, height, detailed=False):
    object_list = []
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    colors = np.asarray(pcd.colors)
    x_min, y_min, z_min = np.min(points, axis=0)
    x_max, y_max, z_max = np.max(points, axis=0)
    print(f"x_min:{x_min} y_min:{y_min} z_min:{z_min}")
    print(f"x_max:{x_max} y_max:{y_max} z_max:{z_max}")
    if detailed == False:
        return
    for i, points in enumerate(tqdm(points, desc="Processing .ply files")):
        if points[2] > height:
            object_name = color_to_object(colors[i], color_info)
            assert (
                object_name != False
            ), f"color_to_object error, object name:{object_name}"
            if object_name != False:
                object_list.appen(object_name)
    print(object_list)
    return object_list


def process_pipeline(
    input_file_path: str,
    output_file_path: str,
    input_point_path: str,
    output_point_path: str,
    need_refine_points_cloud=False,
):
    """`color_dict_path`: store the index to rgb[0-255],\n

    `object_list_path`: store the arma3 object name to index,\n
    it will build `color_info.json` which contains the hex color\n
    to any description in the arma3 object and generate \n
    the `unique_object_json.json` to reduce the \n
    count of the colored object(merge the same object), and generate\n
    object_info.json to meet the need of merge different pointscloud\n
    it can be used to merge description of approximate objects.

    Args:
        color_dict_path (_type_): _description_
        object_list_path (_type_): _description_
    """
    color_info_path = os.path.join(output_file_path, "color_info.json")
    unique_object_json_path = os.path.join(output_file_path, "unique_object_json.json")
    object_info_path = os.path.join(output_file_path, "object_info.json")
    object_list_json_path = os.path.join(output_file_path, "object_list.json")

    color_dict_path = os.path.join(input_file_path, "color_dict.json")
    object_list_path = os.path.join(input_file_path, "object_list.pkl")

    color_dict = load_color_dict(color_dict_path)
    object_list = load_object_list(object_list_path, object_list_json_path)
    build_color_info_json(
        color_dict=color_dict, object_list=object_list, store_file_path=color_info_path
    )
    build_unique_object_json(object_list_path, unique_object_json_path)

    color_info_json = load_ref_json_file(color_info_path)
    color_dict_json = load_ref_json_file(color_dict_path)
    unique_object_json = load_ref_json_file(unique_object_json_path)
    build_object_info_json(
        unique_object_json, color_dict_json, color_info_json, object_info_path
    )
    if need_refine_points_cloud == False:
        return
    refine_colored_point_cloud(
        input_point_path,
        output_point_path,
        color_dict_json,
        color_info_json,
        unique_object_json,
    )


def get_unique_color(color_dict: dict, color: list):
    if color in color_dict.values():
        return color
    while True:
        color = [random.randint(0, 255) for _ in range(3)]
        if color not in color_dict.values():
            return color


def get_new_index(color_dict: dict, index: int):
    if str(index) not in color_dict.keys():
        return index
    max_index = max(color_dict.keys())
    assert max_index <= 255 * 255 * 255 - 1

    set_keys = set(color_dict.keys())
    full_set_keys = set(range(0, max_index + 2))

    missed_keys = full_set_keys - set_keys
    min_set_key = min(missed_keys)
    return min_set_key


def merge_two_object_info(info_path_base, info_path_add, output_object_path):
    color_dict_path_1 = os.path.join(info_path_base, "color_dict.json")
    color_info_path_1 = os.path.join(info_path_base, "color_info.json")
    unique_object_path_1 = os.path.join(info_path_base, "unique_object_json.json")
    object_info_path_1 = os.path.join(info_path_base, "object_info.json")
    object_list_path_1 = os.path.join(info_path_base, "object_list.pkl")

    color_dict_path_2 = os.path.join(info_path_add, "color_dict.json")
    color_info_path_2 = os.path.join(info_path_add, "color_info.json")
    unique_object_path_2 = os.path.join(info_path_add, "unique_object_json.json")
    object_info_path_2 = os.path.join(info_path_add, "object_info.json")
    object_list_path_2 = os.path.join(info_path_add, "object_list.pkl")

    new_color_dict_path = os.path.join(output_object_path, "color_dict.json")
    new_color_info_path = os.path.join(output_object_path, "color_info.json")
    new_unique_object_path = os.path.join(output_object_path, "unique_object_json.json")
    new_object_info_path = os.path.join(output_object_path, "object_info.json")
    new_object_list_path = os.path.join(output_object_path, "object_list.pkl")
    new_object_list_txt_path = os.path.join(output_object_path, "object_list.json")

    print("-" * 20 + "Loading  1  Files" + "-" * 20)
    color_dict_1 = load_color_dict(color_dict_path_1)
    object_list_1 = load_object_list(object_list_path_1)
    color_info_1 = load_ref_json_file(color_info_path_1)
    object_info_1 = load_ref_json_file(object_info_path_1)
    unique_object_json_1 = load_ref_json_file(unique_object_path_1)

    print("-" * 20 + "Loading  2  Files" + "-" * 20)
    color_dict_2 = load_color_dict(color_dict_path_2)
    object_list_2 = load_object_list(object_list_path_2)
    color_info_2 = load_ref_json_file(color_info_path_2)
    object_info_2 = load_ref_json_file(object_info_path_2)
    unique_object_json_2 = load_ref_json_file(unique_object_path_2)

    for object_name, info in object_info_2.items():
        if object_name not in object_info_1:
            new_color = get_unique_color(color_dict_1, info["color"])
            new_index = get_new_index(color_dict_1, int(info["index"]))
            normalize_color = [rgb / 255.0 for rgb in new_color]
            restore_color = [rgb * 255.0 for rgb in normalize_color]
            hex_color_str = rgb_to_hex(new_color)

            new_object = {}
            new_object["color"] = new_color
            new_object["normalize_color"] = normalize_color
            new_object["restore_color"] = restore_color
            new_object["object"] = info["object"]
            new_object["object_name"] = object_name
            new_object["hex_color"] = hex_color_str
            new_object["index"] = new_index
            color_dict_1[str(new_index)] = new_color
            object_list_1.append([info["object"], new_index])
            color_info_1[hex_color_str] = new_object
            object_info_1[object_name] = new_object
            unique_object_json_1[object_name] = new_index

    print("-" * 20 + "Saving new Files" + "-" * 20)
    print(f"New Color Dict saved in {new_color_dict_path}, Len:{len(color_dict_1)}")
    color_dict_1 = {str(k): v for k, v in color_dict_1.items()}
    with open(new_color_dict_path, "w") as out_file:
        json.dump(color_dict_1, out_file, sort_keys=True, indent=4)

    print(f"New Object List saved in {new_object_list_path}, Len:{len(object_list_1)}")
    with open(new_object_list_path, "wb") as file:
        pickle.dump(object_list_1, file)

    print(f"New Color Info saved in {new_color_info_path}, Len:{len(color_info_1)}")
    with open(new_color_info_path, "w") as out_file:
        json.dump(color_info_1, out_file, sort_keys=True, indent=4)

    print(f"New Object Info saved in {new_object_info_path}, Len:{len(object_info_1)}")
    with open(new_object_info_path, "w") as out_file:
        json.dump(object_info_1, out_file, sort_keys=True, indent=4)

    print(
        f"New Unique Object Json saved in {new_unique_object_path}, Len:{len(unique_object_json_1)}"
    )
    with open(new_unique_object_path, "w") as out_file:
        json.dump(unique_object_json_1, out_file, sort_keys=True, indent=4)

    object_list_dict = {}
    for name, index in object_list_1:
        object_list_dict[name] = index
    print(
        f"New Object List Json saved in {new_object_list_txt_path}, Len:{len(object_list_dict)}"
    )
    with open(new_object_list_txt_path, "w") as file:
        json.dump(object_list_dict, file, sort_keys=True, indent=4)
    print("-" * 20 + "      Over!     " + "-" * 20)


def change_points_cloud_color(
    pcd_input_path, pcd_output_path, color_info_path_origin, object_info_path_new
):
    color_info_origin = load_ref_json_file(color_info_path_origin)
    object_info_new = load_ref_json_file(object_info_path_new)
    pcd = o3d.io.read_point_cloud(pcd_input_path)
    color = np.asarray(pcd.colors)
    for i, item in enumerate((tqdm(color, desc="Processing .ply files"))):
        object_name = color_to_object(color[i], color_info_origin)
        assert object_name != False, f"color_to_object error, object name:{object_name}"
        if object_name != False:
            new_color = object_info_new[object_name]["color"]
            color[i] = np.array(new_color) / 255.0
    pcd.colors = o3d.utility.Vector3dVector(color)
    o3d.io.write_point_cloud(pcd_output_path, pcd)


def voxel_point_cloud(input_file: str, output_path: str, color_info: dict, voxel_size):
    pcd = o3d.io.read_point_cloud(input_file)
    object_to_pcd = {}
    points = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    colors = np.asarray(pcd.colors)

    for i, item in enumerate((tqdm(colors, desc="Processing .ply files"))):
        object_name = color_to_object(colors[i], color_info)
        assert object_name != False, f"color_to_object error, object name:{object_name}"
        if object_name != False:
            point_array = points[i]
            normal_array = normals[i]
            color_array = colors[i]

            if object_name not in object_to_pcd.keys():
                object_to_pcd[object_name] = [
                    [point_array],
                    [normal_array],
                    [color_array],
                ]
            else:
                object_to_pcd[object_name][0].append(point_array)
                object_to_pcd[object_name][1].append(normal_array)
                object_to_pcd[object_name][2].append(color_array)

    total_pcd = o3d.geometry.PointCloud()
    for object_name, array in object_to_pcd.items():
        filtered_pcd = o3d.geometry.PointCloud()
        filtered_pcd.points = o3d.utility.Vector3dVector(np.vstack(array[0]))
        filtered_pcd.normals = o3d.utility.Vector3dVector(np.vstack(array[1]))
        filtered_pcd.colors = o3d.utility.Vector3dVector(np.vstack(array[2]))
        filtered_pcd = filtered_pcd.voxel_down_sample(voxel_size)

        total_pcd = total_pcd + filtered_pcd
        file_name = os.path.join(output_path, object_name + ".ply")
        o3d.io.write_point_cloud(file_name, filtered_pcd)
        del filtered_pcd

    file_name = os.path.join(output_path, "Total.ply")
    o3d.io.write_point_cloud(file_name, total_pcd)


logger = setup_logger()
