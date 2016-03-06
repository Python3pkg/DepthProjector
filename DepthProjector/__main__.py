#!/usr/bin/env python

# coding=utf-8

import click
from DepthProjector._pp import PerspectiveProjection

__author__ = 'kanairen'


@click.command()
@click.argument('file_path')
@click.option('--theta_angle_range', '-t', nargs=3, type=(int, int, int),
              default=(0, 360, 30),
              help='Range of theta angle([FROM] [TO] [STEP]). Default is (0 360 30).')
@click.option('--phi_angle_range', '-p', nargs=3, type=(int, int, int),
              default=(-60, 61, 30),
              help='Range of phi angle([FROM] [TO] [STEP]). Default is (-60 61 30).')
@click.option('--init_rotation', '-i', nargs=3, type=(int, int, int),
              default=(0, 0, 0),
              help='Initial rotation of 3d shape([X] [Y] [Z]). Default is (0 0 0).')
@click.option('--radius', '-r', type=float, default=1.,
              help="Radius of camera coordinate.")
@click.option('--is_view_only', '-v', type=bool, default=False,
              help='option whether is DepthProjector executed as 3D Viewer(procjection is not executed) or not.')
def depth_image(file_path, theta_angle_range, phi_angle_range, init_rotation,
                radius, is_view_only):
    pp = PerspectiveProjection(theta_angle_range, phi_angle_range, radius)
    pp.depth_image(file_path, init_rotation, is_view_only=is_view_only)


if __name__ == '__main__':
    depth_image()
