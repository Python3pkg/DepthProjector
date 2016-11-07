#!/usr/bin/env python

# coding=utf-8

import click

from DepthProjector._pp import PerspectiveProjection

__author__ = 'kanairen'

HELP_THETA = 'Range of theta angle([FROM] [TO] [STEP]). Default is (0 360 30).'
HELP_PHI = 'Range of phi angle([FROM] [TO] [STEP]). Default is (-60 61 30).'
HELP_INIT_ROTATION = 'Initial rotation of 3d shape([X] [Y] [Z]). Default is (0 0 0).'
HELP_RADIUS = "Radius of camera coordinate."
HELP_IS_VIEW_ONLY = 'Option whether is DepthProjector executed as 3D Viewer(projection is not executed) or not.'
HELP_SAVE_IMAGE_EXT = 'File extention of depth image. Default is \'.png\' .'


@click.command()
@click.argument('model_file_path', type=str)
@click.argument('theta_from', type=int)
@click.argument('theta_to', type=int)
@click.argument('theta_step', type=int)
@click.argument('phi_from', type=int)
@click.argument('phi_to', type=int)
@click.argument('phi_step', type=int)
@click.argument('save_array_dir', type=str)
@click.argument('save_img_dir', type=str)
@click.option('--save_img_ext', '-e', type=str, default='png',
              help=HELP_SAVE_IMAGE_EXT)
@click.option('--init_rotation', '-i', nargs=3, type=(int, int, int),
              default=(0, 0, 0), help=HELP_INIT_ROTATION)
@click.option('--is_model_centered', type=bool, default=False)
@click.option('--is_model_normalized', type=bool, default=False)
@click.option('--is_view_only', '-v', type=bool, default=False,
              help=HELP_IS_VIEW_ONLY)
@click.option('--window_title', '-wt', type=str, default='')
@click.option('--window_size', '-ws', type=(int, int), default=(300, 300))
@click.option('--window_position', '-wp', type=(int, int), default=(0, 0))
@click.option('--bg_color', '-c', type=(float, float, float, float),
              default=(0., 0.3, 0., 1))
@click.option('--radius', '-r', type=float, default=1., help=HELP_RADIUS)
@click.option('--theta', '-t', type=float, default=0.)
@click.option('--phi', '-p', type=float, default=0.)
@click.option('--fov_y', '-fy', type=float, default=45.)
@click.option('--z_near', '-zn', type=float, default=1.)
@click.option('--z_far', '-zf', type=float, default=10.)
@click.option('--is_viewport_rate_fix', '-v', type=bool, default=True)
def depth_image(model_file_path,
                theta_from, theta_to, theta_step, phi_from, phi_to, phi_step,
                save_array_dir, save_img_dir, save_img_ext,
                init_rotation, is_model_centered, is_model_normalized,
                is_view_only, window_title,
                window_size, window_position, bg_color, radius, theta,
                phi, fov_y, z_near, z_far, is_viewport_rate_fix):
    pp = PerspectiveProjection(model_file_path,
                               (theta_from, theta_to, theta_step),
                               (phi_from, phi_to, phi_step),
                               save_array_dir, save_img_dir, save_img_ext,
                               init_rotation, is_model_centered,
                               is_model_normalized, is_view_only, window_title,
                               window_size, window_position, bg_color, radius,
                               theta,
                               phi, fov_y, z_near, z_far, is_viewport_rate_fix)
    pp.start()
    # pp = PerspectiveProjection(theta_angle_range, phi_angle_range, radius,
    #                            depth_image_ext, window_title='',
    #                            window_size=(300, 300),
    #                            window_position=(0, 0),
    #                            bg_color=(0., 0.3, 0., 1), r=1.,
    #                            theta=0., phi=0., fov_y=45.0, z_near=1.0,
    #                            z_far=10,
    #                            is_viewport_rate_fix=True)
    # pp.depth_image(file_path, init_rotation, is_view_only=is_view_only)


if __name__ == '__main__':
    depth_image()
