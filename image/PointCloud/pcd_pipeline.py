from pcd_process import *





# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# ************************************First to Use to merge same object and remove unused  points*****************************************************

# object_info_input_path = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-1\Object_Info"
# )
# object_info_output_path = (
#     r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-1\Object_Info"
# )
# input_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3\Building"
# output_dir = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3\Filted"
# process_pipeline(object_info_input_path, object_info_output_path, input_dir, output_dir, need_refine_points_cloud=False)

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# *******************************************Merge all points cloud file to a entire file*************************************************************

# input_file_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3\Filted"
# output_file_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3"
# merge_point_cloud(input_file_path, output_file_path)

# ************************************************************End*************************************************************************************
# ---------------------------------------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------------------------------------#
# ***********************************************Used to Reduce points cloud size*********************************************************************

in_file_name = (
    r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Building-2-Filted.ply"
)
out_path_name = (
    r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-2\Building-2-0.1.ply"
)
color_info_path = (
    r"/Users/guoan/Documents/GitHub/Arma3_Depth/Arma3_Forest/color_info.json"
)
color_info = load_ref_json_file(color_info_path)
voxel_point_cloud(in_file_name, out_path_name, color_info, 0.1)

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

# base_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\1-2\Object_Info"
# add_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\Colored-3\Object_Info"
# output_path = r"E:\E_Disk_Files\Arma3_PointCloud\Colored_Building\1-2\Object_Info"
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
