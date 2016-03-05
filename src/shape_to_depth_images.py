# coding: utf-8

import os
import threading
import numpy as np

import src.io as io
import src.config as config
from shape import Obj
from gl import GL

# GL object
GL = GL()

gen_ids = None
gen_theta_angle = None
gen_phi_angle = None

psb_id = None
theta_angle = None
phi_angle = None

is_displayed_since_captured = True
is_capture_called = False


# 形状データセット関数
def set_shape(shape_id, fix_rotate=(0, 0, 0), is_centerized=True):
    # objファイル読み込み
    obj = io.read_obj(
        os.path.join(config.PATH_PSB_OBJ, 'm{}.obj'.format(shape_id)))

    # モデル位置修正
    if is_centerized:
        obj.center()
    obj.rotate(fix_rotate)

    # shapeセット
    GL.shape = obj


def depth_image(ids, theta_angle_range, phi_angle_range, fix_rotate):
    global is_drawn, gen_ids, gen_theta_angle, gen_phi_angle, psb_id, theta_angle, phi_angle

    # 保存先フォルダがない場合、作成
    if not os.path.exists(config.PATH_DEPTH_ARRAY):
        os.makedirs(config.PATH_DEPTH_ARRAY)
    if not os.path.exists(config.PATH_DEPTH_IMG):
        os.makedirs(config.PATH_DEPTH_IMG)

    # ジェネレータ
    gen_ids = (id for id in ids)
    gen_theta_angle = (theta_angle for theta_angle in theta_angle_range)
    gen_phi_angle = (phi_angle for phi_angle in phi_angle_range)

    psb_id = gen_ids.next()
    theta_angle = gen_theta_angle.next()
    phi_angle = gen_phi_angle.next()

    # 深度マップ取得
    def capture(theta_angle, phi_angle):
        global is_capture_called
        # カメラ位置を変更し、描画
        theta = theta_angle * np.pi / 180
        phi = phi_angle * np.pi / 180
        GL.camera_rotate(theta, phi)
        is_capture_called = True

    def update():
        global gen_ids, gen_theta_angle, gen_phi_angle, psb_id, theta_angle, phi_angle

        # 値をジェネレータから取り出す
        try:
            phi_angle = gen_phi_angle.next()
        except StopIteration:
            gen_phi_angle = (phi_angle for phi_angle in phi_angle_range)
            phi_angle = gen_phi_angle.next()
            try:
                theta_angle = gen_theta_angle.next()
            except StopIteration:
                gen_theta_angle = (theta_angle for theta_angle in
                                   theta_angle_range)
                theta_angle = gen_theta_angle.next()
                try:
                    psb_id = gen_ids.next()
                    set_shape(psb_id, fix_rotate)
                except StopIteration:
                    GL.finish()
                    return

    def save():
        global psb_id, theta_angle, phi_angle
        # 描画が完了したら保存
        file_name = 'm{}_t{}_p{}'.format(psb_id, theta_angle, phi_angle)
        path_image = os.path.join(config.PATH_DEPTH_IMG, str(psb_id))
        path_array = os.path.join(config.PATH_DEPTH_ARRAY, str(psb_id))
        GL.save_depthimage(file_name, path=path_image)
        GL.save_deptharray(file_name, path=path_array)

    # OpenGL描画時に呼ばれる関数
    def on_display():
        global is_displayed_since_captured, is_capture_called
        if is_capture_called:
            save()
            update()
            is_capture_called = False
            is_displayed_since_captured = True

    def on_idle():
        global is_displayed_since_captured, is_capture_called
        if is_displayed_since_captured:
            is_displayed_since_captured = False
            # 深度マップのキャプチャ
            run = lambda: capture(theta_angle, phi_angle)
            threading.Thread(target=run).start()

    set_shape(psb_id, fix_rotate)
    GL.display_func = on_display
    GL.idle_func = on_idle
    GL.start()


if __name__ == '__main__':
    psb_ids = sorted(
            [1167, 1169, 1171, 1173, 1175, 1177, 1179, 1181, 1183, 1185, 1187,
             1189, 1191, 1193, 1195, 1197, 1199, 1201, 1203, 1205, 1207, 1209,
             1211, 1213, 1215, 1217, 1219, 1221, 1223, 1225, 1227, 1229, 1231,
             1233, 1235, 1237, 1239, 1241, 1243, 1245, 1247, 1249, 1251, 1253,
             1255, 1257, 1259, 1261, 1263, 1265, 1168, 1170, 1172, 1174, 1176,
             1178, 1180, 1182, 1184, 1186, 1188, 1190, 1192, 1194, 1196, 1198,
             1200, 1202, 1204, 1206, 1208, 1210, 1212, 1214, 1216, 1218, 1220,
             1222, 1224, 1226, 1228, 1230, 1232, 1234, 1236, 1238, 1240, 1242,
             1244, 1246, 1248, 1250, 1252, 1254, 1256, 1258, 1260, 1262, 1264,
             1266, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141,
             143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167,
             169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193,
             195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 118,
             120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144,
             146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170,
             172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196,
             198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 1647, 1649,
             1651, 1653, 1655, 1657, 1659, 1661, 1663, 1665, 1646, 1648, 1650,
             1652, 1654, 1656, 1658, 1660, 1662, 1664, 990, 992, 994, 996,
             998, 1000, 1002, 1004, 1006, 1008, 1010, 1012, 1014, 1016, 1018,
             1020, 1022, 1024, 1026, 1028, 1030, 1032, 1034, 1036, 1038, 989,
             991, 993, 995, 997, 999, 1001, 1003, 1005, 1007, 1009, 1011,
             1013, 1015, 1017, 1019, 1021, 1023, 1025, 1027, 1029, 1031, 1033,
             1035, 1037, 1039, 1303, 1305, 1307, 1309, 1311, 1313, 1315, 1317,
             1319, 1321, 1323, 1325, 1327, 1329, 1331, 1333, 1335, 1302, 1304,
             1306, 1308, 1310, 1312, 1314, 1316, 1318, 1320, 1322, 1324, 1326,
             1328, 1330, 1332, 1334, 1336, 341, 343, 345, 347, 349, 351, 353,
             355, 357, 359, 361, 363, 365, 367, 369, 371, 340, 342, 344, 346,
             348, 350, 352, 354, 356, 358, 360, 362, 364, 366, 368, 370, 526,
             528, 530, 532, 534, 536, 538, 540, 542, 544, 546, 527, 529, 531,
             533, 535, 537, 539, 541, 543, 545, 547, 649, 651, 653, 655, 657,
             659, 661, 663, 665, 667, 648, 650, 652, 654, 656, 658, 660, 662,
             664, 666, 870, 872, 874, 876, 878, 880, 882, 884, 886, 888, 890,
             892, 894, 896, 898, 900, 902, 904, 906, 908, 910, 912, 914, 916,
             918, 920, 871, 873, 875, 877, 879, 881, 883, 885, 887, 889, 891,
             893, 895, 897, 899, 901, 903, 905, 907, 909, 911, 913, 915, 917,
             919, 437, 439, 441, 443, 445, 447, 449, 451, 453, 455, 457, 438,
             440, 442, 444, 446, 448, 450, 452, 454, 456, 218, 220, 222, 224,
             226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250,
             252, 254, 256, 258, 219, 221, 223, 225, 227, 229, 231, 233, 235,
             237, 239, 241, 243, 245, 247, 249, 251, 253, 255, 257, 807, 809,
             811, 813, 815, 817, 819, 821, 823, 825, 827, 808, 810, 812, 814,
             816, 818, 820, 822, 824, 826, 828, 1428, 1430, 1432, 1434, 1436,
             1438, 1440, 1442, 1444, 1446, 1427, 1429, 1431, 1433, 1435, 1437,
             1439, 1441, 1443, 1445, 1447, 688, 690, 692, 694, 696, 698, 700,
             702, 704, 706, 708, 710, 712, 714, 716, 687, 689, 691, 693, 695,
             697, 699, 701, 703, 705, 707, 709, 711, 713, 715, 717, 1147,
             1149, 1151, 1153, 1155, 1157, 1159, 1161, 1163, 1165, 1146, 1148,
             1150, 1152, 1154, 1156, 1158, 1160, 1162, 1164, 1166, 1057, 1059,
             1061, 1063, 1065, 1067, 1069, 1071, 1073, 1075, 1077, 1058, 1060,
             1062, 1064, 1066, 1068, 1070, 1072, 1074, 1076, 1078, 1353, 1355,
             1357, 1359, 1361, 1363, 1365, 1367, 1369, 1371, 1373, 1354, 1356,
             1358, 1360, 1362, 1364, 1366, 1368, 1370, 1372, 1374, 1516, 1518,
             1520, 1522, 1524, 1526, 1528, 1530, 1532, 1534, 1517, 1519, 1521,
             1523, 1525, 1527, 1529, 1531, 1533, 1535, 845, 847, 849, 851,
             853, 855, 857, 859, 861, 863, 865, 867, 869, 844, 846, 848, 850,
             852, 854, 856, 858, 860, 862, 864, 866, 868, 290, 292, 294, 296,
             298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322,
             291, 293, 295, 297, 299, 301, 303, 305, 307, 309, 311, 313, 315,
             317, 319, 321, 1118, 1120, 1122, 1124, 1126, 1128, 1130, 1132,
             1134, 1136, 1138, 1140, 1142, 1144, 1119, 1121, 1123, 1125, 1127,
             1129, 1131, 1133, 1135, 1137, 1139, 1141, 1143, 1145])

    depth_image(psb_ids,
                theta_angle_range=xrange(0, 360, 30),
                phi_angle_range=xrange(-60, 61, 30),
                fix_rotate=(90, 0, 90))
