# coding=utf-8

import sys
from src.pp import depth_image

__author__ = 'kanairen'

if __name__ == '__main__':
    def to_tuple(str):
        return tuple(map(int, str.strip('(').strip(')').split(',')))


    args = sys.argv
    file_name = args[1]
    theta_angle_range = to_tuple(args[2])
    phi_angle_range = to_tuple(args[3])
    fix_rotate = to_tuple(args[4])

    depth_image(file_name, theta_angle_range, phi_angle_range, fix_rotate)
