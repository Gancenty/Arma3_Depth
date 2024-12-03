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
import trimesh
from pcd_process import *


def ply_to_mesh(file_name):
    pcd = o3d.io.read_point_cloud(file_name)
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=12
    )
    o3d.io.write_triangle_mesh(f"{file_name}-Mesh.ply", mesh)
    return mesh


def ply_to_glb(file_name):
    mesh = o3d.io.read_triangle_mesh(file_name)

    vertices = np.asarray(mesh.vertices)
    print(vertices.shape)

    vertex_colors = np.asarray(mesh.vertex_colors)
    print(vertex_colors.shape)

    vertex_normals = np.asarray(mesh.vertex_normals)
    print(vertex_normals.shape)

    triangles = np.asarray(mesh.triangles)
    print(triangles.shape)

    vertices[:, [1, 2]] = vertices[:, [2, 1]]  # 交换 Y 和 Z
    triangles[:, [1, 2]] = triangles[:, [2, 1]]  # 交换 Y 和 Z

    trimesh_mesh = trimesh.Trimesh(
        vertices=vertices,
        # vertex_colors=vertex_colors,
        # vertex_normals=vertex_normals,
        faces=triangles,
    )

    trimesh_mesh.export(f"{file_name}.glb")


def transform_point_cloud(input_path, output_path):
    folder_path = input_path
    ply_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".ply")
    ]

    for filename in tqdm(ply_files, desc="Processing .ply files"):
        file_path = os.path.join(folder_path, filename)
        pcd = o3d.io.read_point_cloud(file_path)
        # max_coord = pcd.get_max_bound()
        # min_coord = pcd.get_min_bound()

        # center_x = (max_coord[0] + min_coord[0]) / 2
        # center_y = (max_coord[1] + min_coord[1]) / 2
        # min_z = min_coord[2]
        offset_coord = np.array([8650.0, 18250.0, 163.65823364])
        print(f"Offset Coord:{offset_coord}")

        points = np.asarray(pcd.points) - offset_coord
        normals = np.asarray(pcd.normals)
        colors = np.asarray(pcd.colors)

        filtered_pcd = o3d.geometry.PointCloud()
        filtered_pcd.points = o3d.utility.Vector3dVector(points)
        filtered_pcd.normals = o3d.utility.Vector3dVector(normals)
        filtered_pcd.colors = o3d.utility.Vector3dVector(colors)

        print("max_bound:", filtered_pcd.get_max_bound())
        print("min_bound:", filtered_pcd.get_min_bound())

        output_file = os.path.join(output_path, f"{filename}-Rectify.ply")
        o3d.io.write_point_cloud(output_file, filtered_pcd)
        # mesh = ply_to_mesh(filtered_pcd, filename)
        # ply_to_glb(mesh, filename)


def load_ply_to_trimesh(file_name):

    mesh = ply_to_mesh(file_name)
    # mesh = o3d.io.read_triangle_mesh(file_name)
    vertices = np.asarray(mesh.vertices)
    triangles = np.asarray(mesh.triangles)

    vertices[:, [1, 2]] = vertices[:, [2, 1]]  # 交换 Y 和 Z
    triangles[:, [1, 2]] = triangles[:, [2, 1]]  # 交换 Y 和 Z

    trimesh_mesh = trimesh.Trimesh(
        vertices=vertices,
        # vertex_colors=vertex_colors,
        # vertex_normals=vertex_normals,
        faces=triangles,
    )
    return trimesh_mesh


def merge_multi_mesh_to_glb(input_floder, output_floder, unique_object_list: list):
    ply_files = [
        filename.split(".", 1)[0]
        for filename in os.listdir(input_floder)
        if filename.endswith(".ply")
    ]

    mesh1 = load_ply_to_trimesh(r"D:\Gancenty\Desktop\Arma3_Controller\@Arma3_Depth\class\mesh\t_fraxinusav2s_f.ply-Rectify.ply")
    mesh2 = load_ply_to_trimesh(r"D:\Gancenty\Desktop\Arma3_Controller\@Arma3_Depth\class\mesh\u_house_big_01_v1_f.ply-Rectify.ply")

    scene = trimesh.Scene()
    # # 加载多个mesh
    # mesh1 = trimesh.load_mesh(
    #     r"D:\Gancenty\Desktop\Arma3_Controller\@Arma3_Depth\class\mesh\t_fraxinusav2s_f.ply-Rectify.ply"
    # )
    # mesh2 = trimesh.load_mesh(
    #     r"D:\Gancenty\Desktop\Arma3_Controller\@Arma3_Depth\class\mesh\t_ficusb2s_f.ply-Rectify.ply"
    # )
    scene.add_geometry(mesh1, geom_name="Mesh1")  # 给mesh1命名为 'Mesh1'
    scene.add_geometry(mesh2, geom_name="Mesh2")  # 给mesh2命名为 'Mesh2'

    # 导出为GLB文件
    scene.export("combined_scene_with_names.glb")
    # for filename in tqdm(ply_files, desc="Processing .ply files"):
    #     file_path = os.path.join(input_floder, filename)
    #     mesh = o3d.io.read_triangle_mesh(input_floder)

    #     scene = trimesh.Scene()
    #     # 加载多个mesh
    #     mesh1 = trimesh.load_mesh('mesh1.obj')
    #     mesh2 = trimesh.load_mesh('mesh2.obj')
    #     scene.add_geometry(mesh1, name='Mesh1')  # 给mesh1命名为 'Mesh1'
    #     scene.add_geometry(mesh2, name='Mesh2')  # 给mesh2命名为 'Mesh2'

    # # 导出为GLB文件
    # scene.export('combined_scene_with_names.glb')

    # vertices = np.asarray(mesh.vertices)
    # print(vertices.shape)

    # vertex_colors = np.asarray(mesh.vertex_colors)
    # print(vertex_colors.shape)

    # vertex_normals = np.asarray(mesh.vertex_normals)
    # print(vertex_normals.shape)

    # triangles = np.asarray(mesh.triangles)
    # print(triangles.shape)

    # vertices[:, [1, 2]] = vertices[:, [2, 1]]  # 交换 Y 和 Z
    # triangles[:, [1, 2]] = triangles[:, [2, 1]]  # 交换 Y 和 Z

    # trimesh_mesh = trimesh.Trimesh(
    #     vertices=vertices,
    #     # vertex_colors=vertex_colors,
    #     # vertex_normals=vertex_normals,
    #     faces=triangles,
    # )


def classify_building_object():
    pass


if __name__ == "__main__":
    # wipe_out_point_cloud("./class", "./class", 8500, 18100, 300, 300, reserved=5, rectify=True)
    # transform_point_cloud("./class", "./class")
    merge_multi_mesh_to_glb("./class/mesh", "./class/glb", None)
    # ply_to_mesh(r"D:\Gancenty\Desktop\Arma3_Controller\@Arma3_Depth\Building-0.1.ply-Rectify.ply")
    # ply_to_glb(
    #     r"D:\Gancenty\Desktop\Arma3_Controller\@Arma3_Depth\Building-0.1.ply-Rectify.ply-Mesh.ply"
    # )
    pass
