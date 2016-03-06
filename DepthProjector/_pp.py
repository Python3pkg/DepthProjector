# coding=utf-8


import sys
import os
import _config
import threading
import numpy as np

from _gl import GL
from _shape_io import read_obj

__author__ = 'kanairen'

"""
perspective-projection
"""

GL = GL()

theta_angle = None
phi_angle = None

gen_angle = None

is_displayed_since_captured = True
is_capture_called = False


def __generate_angle(theta_angle_range, phi_angle_range):
    for t in theta_angle_range:
        for p in phi_angle_range:
            yield (t, p)


def depth_image(shape_file_path, theta_angle_range, phi_angle_range,
                init_rotate):
    global gen_angle

    # 保存先フォルダがない場合、作成
    if not os.path.exists(_config.PATH_DEPTH_ARRAY):
        os.makedirs(_config.PATH_DEPTH_ARRAY)
    if not os.path.exists(_config.PATH_DEPTH_IMG):
        os.makedirs(_config.PATH_DEPTH_IMG)

    gen_angle = __generate_angle(theta_angle_range, phi_angle_range)

    __update()

    set_shape(shape_file_path, init_rotate)

    GL.display_func = __on_display
    GL.idle_func = __on_idle

    GL.start()


def __on_display():
    global is_displayed_since_captured, is_capture_called
    if is_capture_called:
        __save()
        __update()
        is_capture_called = False
        is_displayed_since_captured = True


def __on_idle():
    global is_displayed_since_captured, is_capture_called
    if is_displayed_since_captured and GL.shape:
        is_displayed_since_captured = False
        # 深度マップのキャプチャ
        run = lambda: __capture(theta_angle, phi_angle)
        threading.Thread(target=run).start()


def set_shape(file_path, fix_rotate=None, is_centerized=True,
              is_normalized=True):
    ext = os.path.splitext(file_path)[1]

    if ext == '.obj':

        # objファイル読み込み
        obj = read_obj(file_path)

        # モデル位置修正
        if is_centerized:
            obj.center()
        if is_normalized:
            obj.normal()
        if fix_rotate:
            assert isinstance(fix_rotate, tuple) and len(fix_rotate) == 3
            obj.rotate(fix_rotate)
    else:
        NotImplementedError('the extension of specified path is not supported.')

    # shapeセット
    GL.shape = obj


# 深度マップ取得
def __capture(t_angle, p_angle):
    global is_capture_called
    # カメラ位置を変更し、描画
    theta = t_angle * np.pi / 180.
    phi = p_angle * np.pi / 180.
    GL.camera_rotate(theta, phi)
    is_capture_called = True


def __update():
    global gen_angle, theta_angle, phi_angle
    try:
        theta_angle, phi_angle = gen_angle.next()
    except StopIteration:
        GL.display_func = None
        GL.idle_func = None
        GL.finish()
        return


def __save():
    global theta_angle, phi_angle
    # 描画が完了したら保存
    file_name = 't{}_p{}'.format(theta_angle, phi_angle)
    GL.save_depthimage(file_name)
    GL.save_deptharray(file_name)

