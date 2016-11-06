# coding: utf-8

from DepthProjector._shape import Obj

__author__ = 'kanairen'

import numpy as np


def read_obj(obj_file_path):
    """

    .objファイルを読み込み

    :type obj_file_path : str
    :param obj_file_path: ファイルパス

    :rtype: [np.ndarray, np.ndarray, np.ndarray]
    :return: 頂点配列、法線構成頂点インデックス配列、面構成頂点インデックス配列

    """

    with open(obj_file_path) as f:
        lines = filter(lambda x: x != "\n" and x[0] != "#",
                       [line.strip().split() for line in f.readlines()])

        vertices = np.array(
            [list(map(float, line[1:])) for line in lines if
             line[0] == 'v'])
        normals = np.array(
            [list(map(float, line[1:])) for line in lines if
             line[0] == 'vn'])
        faces = np.array(
            [list(map(lambda x: x - 1,
                      map(int, map(lambda x: x.split('/')[0], line[1:])))) for
             line in lines if line[0] == 'f'])

    return Obj(vertices, normals, faces)


def read_off(off_file_path):
    """

    .off形式のファイルを読み込み

    :type off_file_path: str
    :param off_file_path: .offファイル名

    :rtype: [np.ndarray, np.ndarray, np.ndarray]
    :return: 頂点配列、法線構成頂点インデックス配列、面構成頂点インデックス配列


    """

    with open(off_file_path) as f:
        # コメント・空行を除去
        lines = filter(lambda x: x != '\n' and x[0] != "#",
                       f.readlines())

        # 一行目はファイルフォーマット名
        if "OFF" not in lines.pop(0):
            raise IOError("file must be \"off\" format file.")

        # 頂点数、面数、辺数
        n_vertices, n_faces, n_edges = map(int, lines.pop(0).split(' '))

        # 頂点座標を取得
        vertices = np.array([map(float, lines[i].strip().split(' '))
                             for i in xrange(n_vertices)])

        # 面を構成する頂点のインデックス
        faces = np.array(
            [map(int, lines[n_vertices + i].strip().split(' '))[1:]
             for i in xrange(n_faces)])

    return Obj(vertices, np.empty(shape=[0, ]), faces)
