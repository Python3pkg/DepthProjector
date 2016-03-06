#!/usr/bin/env python

# coding=utf-8

import click
from DepthProjector._pp import PerspectiveProjection

__author__ = 'kanairen'


@click.command()
@click.argument('file_path')
@click.argument('theta_angle_range')
@click.argument('phi_angle_range')
@click.argument('init_rotation')
@click.option('--radius', '-r', type=float, default=1.,
              help="Radius of camera coordinate.")
def depth_image(file_path, theta_angle_range, phi_angle_range, init_rotation,
                r):
    pp = PerspectiveProjection(to_tuple(theta_angle_range),
                               to_tuple(phi_angle_range),
                               r)

    pp.depth_image(file_path, to_tuple(init_rotation))


def to_tuple(s):
    return tuple(map(int, s.strip('(').strip(')').split(',')))


if __name__ == '__main__':
    depth_image()
