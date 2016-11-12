#!/usr/bin/env python
# coding:utf8

import os
import sys

import numpy as np

'''

6方向からモデルの透視投影深度画像を取得する

'''

if __name__ == '__main__':

    python_path, off_dir, save_array_path, save_img_path, \
    fy, width, height = sys.argv[1:8]
    is_perspective = sys.argv[8]
    if is_perspective == "True":
        is_perspective = True
    elif is_perspective == "False":
        is_perspective = False
    else:
        raise TypeError
    fy = float(fy)

    rate = 1. / np.sin(fy / 2. / 180. * np.pi)
    r = rate * np.cos(fy / 2. / 180. * np.pi) + 1
    zn = r - 1
    zf = r + 1

    command = "{python_path} ../DepthProjector ".format(python_path=python_path) + \
              "{off_path} {t_from} {t_to} {t_step} {p_from} {p_to} {p_step} " + \
              "{save_array_path}".format(save_array_path=save_array_path) + \
              "/array/{name}/{angle} " + \
              "{save_img_path}".format(save_img_path=save_img_path) + \
              "/img/{name}/{angle} " + \
              "-r {r} -fy {fy} -zn {zn} -zf {zf} -ws {width} {height}" \
                  .format(r=r, fy=fy, zn=zn, zf=zf, width=int(width),
                          height=int(height))

    for f in os.listdir(off_dir):
        for alpha in xrange(0, 45 + 1, 5):
            off_path = os.path.join(off_dir, f)
            name, _ = os.path.splitext(f)

            tf, tt, ts = [alpha, 270 + alpha + 1, 90]
            pf, pt, ps = [0, 1, 90]
            os.system(command.format(off_path=off_path,
                                     t_from=tf, t_to=tt, t_step=ts,
                                     p_from=pf, p_to=pt, p_step=ps,
                                     name=name, angle="{}".format(alpha)))
            tf, tt, ts = [0, 1, 90]
            pf, pt, ps = [270 + alpha, 450 + alpha + 1, 180]
            os.system(command.format(off_path=off_path,
                                     t_from=tf, t_to=tt, t_step=ts,
                                     p_from=pf, p_to=pt, p_step=ps,
                                     name=name, angle="{}".format(alpha)))
