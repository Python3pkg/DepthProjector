# coding=utf-8


import os
import threading

import numpy as np

from _gl import GL
from _shape_io import read_obj, read_off

__author__ = 'kanairen'


class PerspectiveProjection(object):
    """
    perspective-projection
    """

    SAVE_FORMAT = 't{}_p{}'

    def __init__(self, model_file_path, theta_angle_range, phi_angle_range,
                 save_array_dir, save_img_dir, save_img_ext='png',
                 init_rotation=(0, 0, 0), is_model_centered=True,
                 is_model_normalized=True, is_view_only=False,
                 window_title='', window_size=(300, 300),
                 window_position=(0, 0), bg_color=(0., 0.3, 0., 1), r=1.,
                 theta=0., phi=0., fov_y=45.0, z_near=1.0, z_far=10,
                 is_viewport_rate_fix=True):

        gl_shape = self.__load_shape(model_file_path,
                                     init_rotation=init_rotation,
                                     is_centered=is_model_centered,
                                     is_normalized=is_model_normalized)

        self.gl = GL(gl_shape, window_title, window_size, window_position,
                     bg_color, r, theta, phi, fov_y, z_near, z_far,
                     is_viewport_rate_fix)

        if not is_view_only:
            self.gl.display_func = self.__on_display
            self.gl.idle_func = self.__on_idle

        self.theta_angle = None
        self.phi_angle = None

        self.gen_angle = self.__generate_angle(theta_angle_range,
                                               phi_angle_range)

        self.is_displayed_since_captured = True
        self.is_capture_called = False

        # 保存先フォルダがない場合、作成
        if not os.path.exists(save_array_dir):
            os.makedirs(save_array_dir)
        if not os.path.exists(save_img_dir):
            os.makedirs(save_img_dir)

        self.save_array_dir = save_array_dir
        self.save_img_dir = save_img_dir
        self.save_img_ext = save_img_ext

    @staticmethod
    def __generate_angle(theta_angle_range, phi_angle_range):
        for t in xrange(*theta_angle_range):
            for p in xrange(*phi_angle_range):
                yield (t, p)

    def start(self):
        self.gl.start()

    def __update(self):
        try:
            self.theta_angle, self.phi_angle = self.gen_angle.next()
        except StopIteration:
            self.gl.display_func = None
            self.gl.idle_func = None
            self.gl.finish()
            return

    def __load_shape(self, file_path, init_rotation=None, is_centered=True,
                     is_normalized=True):
        ext = os.path.splitext(file_path)[1]

        if ext == '.obj':
            # objファイル読み込み
            obj = read_obj(file_path)
        elif ext == '.off':
            # offファイル読み込み
            obj = read_off(file_path)
        else:
            raise NotImplementedError(
                'the extension of specified path is not supported.')

        # モデル位置修正
        if is_centered:
            obj.center()
        if is_normalized:
            obj.normal()
        if init_rotation is not None:
            assert isinstance(init_rotation, tuple) and len(init_rotation) == 3
            obj.rotate(init_rotation)

        return obj

    def __on_display(self):
        if self.is_capture_called:
            self.__save()
            self.is_capture_called = False
            self.is_displayed_since_captured = True

    def __on_idle(self):
        if self.is_displayed_since_captured and self.gl.shape:
            self.is_displayed_since_captured = False
            self.__update()
            # 深度マップのキャプチャ
            threading.Thread(target=self.__capture).start()

    # 深度マップ取得
    def __capture(self):
        # カメラ位置を変更し、描画
        theta = self.theta_angle * np.pi / 180.
        phi = self.phi_angle * np.pi / 180.
        self.gl.camera_rotate(theta, phi)
        self.is_capture_called = True

    def __save(self):
        # 描画が完了したら保存
        file_name = PerspectiveProjection.SAVE_FORMAT.format(self.theta_angle,
                                                             self.phi_angle)
        self.gl.save_depthimage(os.path.join(self.save_img_dir,
                                             file_name + '.' + self.save_img_ext))
        self.gl.save_deptharray(os.path.join(self.save_array_dir, file_name))
