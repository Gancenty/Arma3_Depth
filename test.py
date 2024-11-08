# import random
# import json
# import os

# # 定义字典文件路径
# file_path = "color_dict.json"

# # 加载或初始化颜色字典
# def load_color_dict():
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             color_dict = json.load(file)
#             # 转换所有值为列表格式（防止 json 中的数字被误解析）
#             color_dict = {int(k): v for k, v in color_dict.items()}
#             return color_dict
#     else:
#         return {}

# # 保存颜色字典到文件
# def save_color_dict(color_dict):
#     with open(file_path, 'w') as file:
#         json.dump(color_dict, file)

# # 生成唯一的 RGB 颜色
# def get_unique_color(color_dict, index):
#     if index not in color_dict:
#         while True:
#             # 生成随机 RGB 颜色
#             color = [random.randint(0, 255) for _ in range(3)]
#             # 检查颜色是否已经存在
#             if color not in color_dict.values():
#                 color_dict[index] = color
#                 break
#     return color_dict[index]

# # 主程序逻辑
# color_dict = load_color_dict()  # 加载已有字典或初始化新字典

# # 示例：添加或获取颜色
# print(get_unique_color(color_dict, 0))  # 新增或获取颜色，映射到序号0
# print(get_unique_color(color_dict, 1))  # 新增或获取颜色，映射到序号1
# print(get_unique_color(color_dict, 2))  # 新增或获取颜色，映射到序号2

# # 程序结束时保存字典
# save_color_dict(color_dict)

# # 打印最终字典
# print(color_dict)
import numpy as np
a = [["580905: stone_pillar_f.p3d",15],["581043: stone_8m_f.p3d",23],["581047: stone_8m_f.p3d",26],["581048: stone_8m_f.p3d",42],["1f8da64c100# 581179: i_stone_housebig_v2_f.p3d Land_i_Stone_HouseBig_V2_F",50],["581382: stone_8m_f.p3d",60],["581088: pavement_narrow_f.p3d",95],["1f8da293580# 580902: u_house_big_01_v1_f.p3d Land_u_House_Big_01_V1_F",106],["580953: b_ficusc1s_f.p3d",125],["580954: b_ficusc1s_f.p3d",127],["1779849: water_source_f.p3d",141],["579930: pavement_wide_f.p3d",150],["1f8a8294100# 579911: powerpolewooden_l_f.p3d Land_PowerPoleWooden_L_F",168],["579705: cratesshabby_f.p3d",176],["579839: pavement_narrow_f.p3d",188],["51973: signt_infofirstaid.p3d",205],["581029: b_ficusc1s_f.p3d",21],["580903: stone_pillar_f.p3d",51],["51980: signt_infohotel.p3d",70],["580884: bench_02_f.p3d",105],["580931: cratesplastic_f.p3d",108],["580930: cratesshabby_f.p3d",109],["580985: pavement_narrow_f.p3d",112],["580911: stone_8m_f.p3d",118],["580895: pavement_wide_f.p3d",137],["579860: b_ficusc1s_f.p3d",167],["579844: pavement_narrow_f.p3d",181],["579832: pavement_wide_corner_f.p3d",196],["579852: pavement_narrow_f.p3d",198],["580848: pavement_wide_f.p3d",214],["1f8da47a080# 580874: u_addon_02_v1_f.p3d Land_u_Addon_02_V1_F",12],["581049: stone_8m_f.p3d",31],["581044: stone_8m_f.p3d",33],["580913: stone_8m_f.p3d",34],["581121: stone_8m_f.p3d",55],["581386: stone_pillar_f.p3d",66],["581127: stone_pillar_f.p3d",74],["580915: stone_8m_f.p3d",104],["1f8a827d600# 580014: i_house_big_01_v3_f.p3d Land_i_House_Big_01_V3_F",139],["579931: pavement_wide_f.p3d",145],["51976: signt_inforestaurant.p3d",160],["579862: b_ficusc1s_f.p3d",164],["580799: barrelsand_f.p3d",210],["581046: stone_8m_f.p3d",16],["581054: stone_8m_f.p3d",20],["581118: stone_8m_f.p3d",37],["581083: t_oleae2s_f.p3d",38],["581162: b_ficusc1s_f.p3d",58],["581146: b_ficusc2s_f.p3d",64],["581111: stone_8m_f.p3d",77],["580974: pavement_narrow_f.p3d",85],["580901: t_ficusb2s_f.p3d",97],["581099: stone_8m_f.p3d",103],["580971: pavement_narrow_corner_f.p3d",110],["579861: b_ficusc1s_f.p3d",175],["580837: pavement_wide_f.p3d",208],["580841: pavement_wide_f.p3d",7],["581038: powerpolewooden_small_f.p3d",28],["581082: stone_pillar_f.p3d",30],["581169: b_ficusc1s_f.p3d",63],["581171: b_ficusc1s_f.p3d",71],["581165: b_ficusc1s_f.p3d",76],["581109: stone_8m_f.p3d",81],["581396: b_ficusc1s_f.p3d",86],["581087: pavement_narrow_f.p3d",94],["581172: pavement_narrow_corner_f.p3d",96],["580893: pavement_wide_f.p3d",116],["580952: b_ficusc1s_f.p3d",119],["580882: pipes_small_f.p3d",121],["580011: cratesplastic_f.p3d",146],["579896: stone_8md_f.p3d",185],["580842: pavement_wide_f.p3d",195],["580845: pavement_wide_f.p3d",202],["1f8a8296b00# 580822: u_house_big_01_v1_f.p3d Land_u_House_Big_01_V1_F",2],["51977: signt_sharpbendleft.p3d",25],["580918: stone_8m_f.p3d",44],["581322: t_oleae2s_f.p3d",45],["582212: stone_8m_f.p3d",120],["580972: pavement_narrow_f.p3d",122],["1f8da294b80# 580962: i_addon_03_v1_f.p3d Land_i_Addon_03_V1_F",140],["579908: stone_pillar_f.p3d",171],["579877: stone_8m_f.p3d",172],["579871: pavement_narrow_corner_f.p3d",193],["579853: pavement_narrow_f.p3d",194],["580791: bench_01_f.p3d",19],["581321: t_oleae2s_f.p3d",47],["1f8da824b80# 581377: metal_shed_f.p3d Land_Metal_Shed_F",49],["580975: pavement_narrow_f.p3d",87],["1f8da643580# 581173: i_stone_housesmall_v1_f.p3d Land_i_Stone_HouseSmall_V1_F",102],["580987: pavement_narrow_f.p3d",111],["580879: t_oleae2s_f.p3d",114],["580990: pavement_narrow_f.p3d",115],["580973: pavement_narrow_f.p3d",128],["580939: t_fraxinusav2s_f.p3d",132],["580894: pavement_wide_f.p3d",142],["579824: t_quercusir2s_f.p3d",156],["579965: t_ficusb2s_f.p3d",157],["579885: stone_8m_f.p3d",187],["579851: pavement_narrow_f.p3d",204],["580838: pavement_wide_f.p3d",1],["580872: t_fraxinusav2s_f.p3d",3],["581144: b_ficusc2s_f.p3d",69],["581163: b_ficusc1s_f.p3d",78],["582250: b_ficusc1s_f.p3d",126],["1f8d9f14b80# 580010: d_house_big_02_v1_f.p3d Land_d_House_Big_02_V1_F",153],["579899: t_ficusb2s_f.p3d",162],["51955: signt_noparking.p3d",169],["579879: stone_8m_f.p3d",170],["579837: pavement_narrow_f.p3d",192],["1f8a8296080# 580835: i_shop_01_v2_f.p3d Land_i_Shop_01_V2_F",209],["580920: stone_4m_f.p3d",9],["581074: stone_8md_f.p3d",17],["581337: stone_8m_f.p3d",18],["581120: stone_8m_f.p3d",46],["581128: stone_pillar_f.p3d",65],["581164: b_ficusc1s_f.p3d",72],["581094: pavement_narrow_f.p3d",93],["1f8da294100# 580963: i_addon_03_v1_f.p3d Land_i_Addon_03_V1_F",107],["579939: pavement_wide_corner_f.p3d",152],["1f8a829b580# 579624: i_stone_housesmall_v1_f.p3d Land_i_Stone_HouseSmall_V1_F",163],["1f8a8294b80# 579834: stone_gate_f.p3d Land_Stone_Gate_F",173],["579841: pavement_narrow_f.p3d",184],["1f8da0f2b00# 579891: u_house_big_01_v1_f.p3d Land_u_House_Big_01_V1_F",191],["1f8a8297580# 580795: i_house_big_01_v2_f.p3d Land_i_House_Big_01_V2_F",197],["580846: pavement_wide_f.p3d",199],["579892: lampstreet_small_off_f.p3d",200],["580836: pavement_wide_f.p3d",206],["1f8a82b3580# 580823: u_house_big_01_v1_f.p3d Land_u_House_Big_01_V1_F",5],["580794: t_quercusir2s_f.p3d",11],["581081: stone_pillar_f.p3d",24],["580957: b_ficusc1s_f.p3d",35],["581051: stone_8m_f.p3d",43],["581381: stone_8m_f.p3d",73],["580976: pavement_narrow_f.p3d",88],["1f8da479600# 580924: i_house_small_01_v2_f.p3d Land_i_House_Small_01_V2_F",100],["580988: pavement_narrow_f.p3d",113],["580880: pallet_vertical_f.p3d",117],["579929: pavement_wide_f.p3d",147],["579706: garbagebin_01_f.p3d",178],["579845: pavement_narrow_f.p3d",180],["579843: pavement_narrow_f.p3d",183],["579838: pavement_narrow_f.p3d",190],["580877: atm_02_f.p3d",207],["580840: pavement_wide_f.p3d",6],["581057: t_ficusb2s_f.p3d",10],["581112: stone_8m_f.p3d",56],["581383: stone_8m_f.p3d",57],["581425: mound01_8m_f.p3d",84],["580986: pavement_narrow_f.p3d",124],["580935: pallets_f.p3d",135],["1f8da0f0b80# 579953: kiosk_blueking_f.p3d Land_Kiosk_blueking_F",136],["580938: basket_f.p3d",138],["580960: b_ficusc1s_f.p3d",165],["579884: stone_8m_f.p3d",179],["1f8d9f16080# 579836: u_house_small_01_v1_f.p3d Land_u_House_Small_01_V1_F",182],["51957: signt_stop.p3d",201],["580830: powerpolewooden_f.p3d",213],["1f8a8295600# 580968: lampstreet_small_f.p3d Land_LampStreet_small_F",8],["1f8da64e080# 581036: i_garage_v2_f.p3d Land_i_Garage_V2_F",13],["581045: stone_8m_f.p3d",32],["580959: b_ficusc1s_f.p3d",40],["581096: stone_8m_f.p3d",80],["581129: stone_pillar_f.p3d",101],["1f8da292b00# 580925: u_house_big_02_v1_f.p3d Land_u_House_Big_02_V1_F",123],["1f8da295600# 580961: i_addon_03mid_v1_f.p3d Land_i_Addon_03mid_V1_F",149],["579934: pavement_wide_f.p3d",151],["580943: garbagebin_01_f.p3d",154],["579856: t_fraxinusav2s_f.p3d",158],["579840: pavement_narrow_f.p3d",186],["580839: pavement_wide_f.p3d",211],["<NULL-object>",0],["581058: t_ficusb2s_f.p3d",14],["580904: stone_pillar_f.p3d",29],["580958: b_ficusc1s_f.p3d",36],["581126: stone_pillar_f.p3d",53],["1f8da64cb80# 581143: i_stone_shed_v1_f.p3d Land_i_Stone_Shed_V1_F",54],["581170: b_ficusc1s_f.p3d",61],["581149: powerpolewooden_f.p3d",67],["581122: stone_8m_f.p3d",75],["580977: pavement_narrow_f.p3d",90],["580979: pavement_narrow_f.p3d",92],["581113: stone_8m_f.p3d",98],["581136: stone_pillar_f.p3d",99],["1f8da292080# 580965: i_shop_02_v2_f.p3d Land_i_Shop_02_V2_F",130],["580896: pavement_wide_f.p3d",134],["580937: chairplastic_f.p3d",148],["579878: stone_8m_f.p3d",166],["580871: t_fraxinusav2s_f.p3d",4],["581030: b_ficusc1s_f.p3d",22],["581077: stone_pillar_f.p3d",41],["581145: b_ficusc2s_f.p3d",59],["581161: b_ficusc1s_f.p3d",68],["580897: pavement_wide_f.p3d",129],["1512568: phonebooth_01_f.p3d",131],["580945: lampdecor_off_f.p3d",133],["580928: barrelsand_f.p3d",144],["1f8a827cb80# 580964: i_addon_03_v1_f.p3d Land_i_Addon_03_V1_F",155],["51958: signt_speedlimit30.p3d",174],["1f8dad2e080# 579663: i_house_big_01_v3_f.p3d Land_i_House_Big_01_V3_F",177],["581042: stone_8m_f.p3d",27],["581060: t_fraxinusav2s_f.p3d",39],["581027: b_ficusc1s_f.p3d",48],["581119: stone_8m_f.p3d",52],["581384: stone_8m_f.p3d",62],["581095: stone_8m_f.p3d",79],["581133: stone_pillar_f.p3d",82],["581110: stone_8m_f.p3d",83],["581140: t_ficusb2s_f.p3d",89],["580978: pavement_narrow_f.p3d",91],["580936: bucket_f.p3d",143],["579964: t_ficusb2s_f.p3d",159],["579876: stone_8m_f.p3d",161],["579858: t_oleae1s_f.p3d",189],["579912: bench_01_f.p3d",203],["51974: signt_infotaxirank.p3d",212]]

print(len(a))