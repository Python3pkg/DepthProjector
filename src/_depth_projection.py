#!/usr/bin/env python

# coding=utf-8

import click
import src._pp as pp

__author__ = 'kanairen'


@click.command()
@click.argument('file_path')
@click.argument('theta_angle_range')
@click.argument('phi_angle_range')
@click.argument('init_rotation')
def depth_image(file_path, theta_angle_range, phi_angle_range, init_rotation):
    pp.depth_image(file_path,
                   to_tuple(theta_angle_range),
                   to_tuple(phi_angle_range),
                   to_tuple(init_rotation))


def to_tuple(s):
    return tuple(map(int, s.strip('(').strip(')').split(',')))


if __name__ == '__main__':
    depth_image()
