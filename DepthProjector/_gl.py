# coding: utf-8

import datetime
import itertools

import PIL.Image as Image
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from DepthProjector._shape import Obj


class GL(object):
    MOUSE_ROTATE_RATE = 0.01
    MOUSE_ZOOM_RATE = 0.01
    GL_UNDEFINED_DISTANCE_VALUE = -1.

    def __init__(self, shape, window_title='', window_size=(300, 300),
                 window_position=(0, 0), bg_color=(0., 0.3, 0., 1), r=1.,
                 theta=0., phi=0., fov_y=45.0, z_near=1.0, z_far=10,
                 is_viewport_rate_fix=True, undefined_dist_value=-1.,
                 is_perspective=True):

        self.shape = shape

        self.window_title = window_title
        self.window_size = window_size
        self.window_position = window_position
        self.bg_color = bg_color

        # カメラパラメタ
        self.r = r  # 半径
        self.theta = theta  # xy平面上での角度
        self.phi = phi  # xy平面上の径とz軸で張られる平面上の角度
        self.camera_aim = [0., 0., 0.]  # カメラエイム
        self.camera_upper = [0., 0., 1.]  # カメラの上方向ベクトル
        self.fov_y = fov_y  # 実視野角
        self.z_near = z_near  # near平面までの距離
        self.z_far = z_far  # far平面までの距離

        # マウスリスナ用変数
        self.prev_x = None
        self.prev_y = None
        self.mouse_button = None
        self.mouse_state = None

        # ビューポートの比率を初期値に固定するかどうか
        self.is_viewport_rate_fix = is_viewport_rate_fix

        # 外部リスナー関数
        self.display_func = None
        self.reshape_func = None
        self.mouse_func = None
        self.motion_func = None
        self.keyboard_func = None
        self.idle_func = None

        self.undefined_dist_value = undefined_dist_value

        self.is_perspective = is_perspective

    def start(self):
        """
        GLメイン関数
        """

        # OpenGL/GLUT環境の初期化
        glutInit(sys.argv)
        # ディスプレイ表示モード
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
        # ウィンドウのサイズ
        glutInitWindowSize(*self.window_size)
        # ウィンドウの位置（左上）
        glutInitWindowPosition(*self.window_position)
        # ウィンドウ起動
        glutCreateWindow(self.window_title)

        # 描画時リスナー
        glutDisplayFunc(self.__display_func)
        # ウィンドウリサイズリスナー
        glutReshapeFunc(self.__reshape_func)
        # マウスリスナー
        glutMouseFunc(self.__mouse_func)
        # マウスドラッグリスナー
        glutMotionFunc(self.__motion_func)
        # キーボードリスナー
        glutKeyboardFunc(self.__keyboard_func)
        # アイドルタイム時リスナー
        glutIdleFunc(self.__idle_func)

        # glClearで塗りつぶす色を設定
        glClearColor(*self.bg_color)
        # Zバッファを有効化
        glEnable(GL_DEPTH_TEST)
        # メインループ終了時にプロセスが死なないようにする
        if glutSetOption:
            glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE,
                          GLUT_ACTION_GLUTMAINLOOP_RETURNS)

        # メインスレッドのループ
        glutMainLoop()

    def __display_func(self):
        """
        描画処理時リスナー
        """
        # glClearColorで指定した色で塗りつぶし
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 初期行列に単位行列を掛け、初期化
        glLoadIdentity()

        # 投影法の設定
        if self.is_perspective:
            # 透視投影
            gluPerspective(self.fov_y,
                           glutGet(GLUT_WINDOW_WIDTH) / glutGet(
                               GLUT_WINDOW_HEIGHT),
                           self.z_near, self.z_far)
        else:
            # 平行投影
            glOrtho(-1.0, 1.0, -1.0, 1.0, self.z_near, self.z_far)

        # カメラ位置、エイム、カメラ上方向を設定
        gluLookAt(
            *itertools.chain(
                self.__rectangular_coordinates(self.r, self.theta,
                                               self.phi),
                self.camera_aim,
                self.camera_upper))

        # モデル描画
        self.__draw()

        if self.display_func:
            self.display_func()

    @staticmethod
    def __rectangular_coordinates(r, theta, phi):
        """
        球面座標から三次元空間座標系
        :param r: 球面半径
        :param theta: xy平面上の角度
        :param phi: theta角上の軸とz軸の張る平面上の角度
        :return: 三次元空間座標系(x,y,z)
        """
        rx = r * np.cos(phi) * np.cos(theta)
        ry = rx * np.tan(theta)
        rz = r * np.sin(phi)
        return rx, ry, rz

    def __draw(self):
        """
        描画関数
        モデルの読み込み元毎に描画方法を切り替える
        """

        if isinstance(self.shape, Obj):
            # 描画方法指定
            glBegin(GL_TRIANGLES)
            for face, c in zip(self.shape.faces, self.shape.colors):
                for v in self.shape.vertices[face]:
                    glVertex3d(*v)
            glEnd()
        glFlush()

    def __reshape_func(self, w, h):
        """
        ディスプレイサイズ変更時リスナー
        :param w: ディスプレイ幅
        :param h: ディスプレイ高さ
        """
        # ビューポート（画面中の描画領域）を指定
        if self.is_viewport_rate_fix:
            # 縦横比固定
            if w > h:
                box = ((w - h) / 2, 0, h, h)
            else:
                box = (0, (h - w) / 2, w, w)
        else:
            box = (0, 0, w, h)

        glViewport(*box)

        if self.reshape_func:
            self.reshape_func(w, h)

    def __mouse_func(self, button, state, x, y):
        """
        マウスリスナー
        :param button: アクションボタンの種類
        :param state: アクションボタンの状態
        :param x: アクションが発生したx座標
        :param y: アクションが発生したy座標
        """
        self.mouse_button = button
        self.mouse_state = state
        self.prev_x = x
        self.prev_y = y
        if self.mouse_func:
            self.mouse_func(button, state, x, y)

    def __motion_func(self, x, y):
        """
        マウスドラッグリスナー
        :param x: アクションが発生したx座標
        :param y: アクションが発生したy座標
        """

        if self.prev_x and self.prev_y and self.mouse_state == GLUT_DOWN:
            if self.mouse_button == GLUT_LEFT_BUTTON:
                # 左ボタンの場合、上下左右ドラッグでカメラを動かす
                t = self.theta + (self.prev_x - x) * self.MOUSE_ROTATE_RATE
                p = self.phi + (y - self.prev_y) * self.MOUSE_ROTATE_RATE
                self.camera_rotate(t, p)
            elif self.mouse_button == GLUT_RIGHT_BUTTON:
                # 右ボタンの場合、上下ドラッグでズームコントロール
                r = self.r + (y - self.prev_y) * self.MOUSE_ZOOM_RATE
                self.camera_zoom(r)

        self.prev_x = x
        self.prev_y = y

        if self.motion_func:
            self.motion_func(x, y)

    def camera_rotate(self, t, p):
        """
        球面座標上のカメラ位置を変更
        :param t: xy平面上での角度
        :param p: xy平面上の径とz軸で張られる平面上の角度
        """
        self.theta = t
        self.phi = p
        glutPostRedisplay()

    def camera_zoom(self, r):
        """
        球面座標の径を変更
        :param r: 球面座標の径
        """
        self.r = r
        glutPostRedisplay()

    def __keyboard_func(self, key, x, y):
        """
        キーボードリスナー
        :param key: 押されたキー文字
        :param x: キーが押された時のx座標
        :param y: キーが押された時のy座標
        """
        if key == 's':
            # 現時点でウィンドウに描画された深度マップを保存
            self.save_deptharray("{}".format(datetime.datetime.now()))
        if key == 'i':
            self.save_depthimage("{}".format(datetime.datetime.now()))

        if self.keyboard_func:
            self.keyboard_func(key, x, y)

    def save_deptharray(self, save_path):
        """

        ウィンドウへの描画に対応する深度マップをnumpy配列として保存する

        :type save_path: str
        :param save_path: 画像を保存するフォルダパス

        """
        np.save(save_path, self.__depth_pixels())

    def save_depthimage(self, save_path):
        """

        ウィンドウへの描画に対応する深度マップを画像として保存する

        :type save_path: str
        :param save_path: 画像保存パス

        """
        depth_map = ((1. - self.__depth_pixels()) * 255).astype(np.uint8)
        Image.fromarray(depth_map).save(save_path)

    def __depth_pixels(self):
        """
        デプスバッファから各座標の深度値を取得する
        :return: 深度値numpy配列
        """
        # ビューポートの領域を取得
        x, y, w, h = glGetIntegerv(GL_VIEWPORT)
        dp = glReadPixelsf(x, y, w, h, GL_DEPTH_COMPONENT)[-1::-1]
        # 任意の未定義距離値を適用
        if GL.GL_UNDEFINED_DISTANCE_VALUE != self.undefined_dist_value:
            dp[dp == GL.GL_UNDEFINED_DISTANCE_VALUE] = self.undefined_dist_value
        return dp

    def __idle_func(self):
        """
        アイドル時のリスナー
        """
        if self.idle_func:
            self.idle_func()

    def finish(self):
        """
        GLUTのメインループを終了する
        """

        if glutLeaveMainLoop:
            glutLeaveMainLoop()
