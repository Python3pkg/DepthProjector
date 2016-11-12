#!/usr/bin/env python
# coding: utf-8

'''

create_six_angle_depth_map.pyで生成した、階層構造になった深度マップを
一つのnpyファイルにまとめる

'''

import os
import re
import sys
import time
import numpy as np

if __name__ == '__main__':

    dir_path, save_array_path = sys.argv[1:]

    # 整数抜き出し用正規表現
    c = re.compile("\d+")

    def sort_str(s_iter):
        perm = np.argsort([int(c.findall(s)[0]) for s in s_iter])
        return np.asarray(s_iter)[perm].astype(np.string_)

    # T*フォルダをモデルIDの昇順にソート
    s_folders = sort_str(os.listdir(dir_path))

    empty = None

    for i, folder in enumerate(s_folders):

        print folder

        # DataAugmentation角度別フォルダを角度の昇順にソート
        s_angles = sort_str(os.listdir(os.path.join(dir_path, folder)))

        start = time.clock()

        for j, angle in enumerate(s_angles):

            # theta-phiの回転角をソート
            file_names = os.listdir(os.path.join(dir_path, folder, angle))
            tp_angles = [map(int, c.findall(name)) for name in file_names]
            tp_angles.sort(key=lambda x: (x[0], x[1]))
            file_names = ["t{}_p{}.npy".format(t, p) for t, p in tp_angles]

            for k, tp_angle in enumerate(file_names):
                path = os.path.join(dir_path, folder, angle, tp_angle)
                arr = np.load(path)

                if empty is None:
                    width, height = arr.shape
                    empty = np.empty(
                        (len(s_folders) * len(s_angles), width, height))

                empty[i * len(s_angles) + j, k, :, :] = arr

        print "{}s".format(time.clock() - start)

    np.save(save_array_path, empty)
