# coding: utf-8

from DepthProjector._shape import Obj

__author__ = 'kanairen'

import numpy as np


def read_obj(file_path):
    """
    objファイルを読み込み、頂点情報、法線情報、面情報を取得
    :param file_path: ファイルパス
    :return: 頂点リスト、法線リスト、面リスト
    """
    # 10.41s/10000time(v=298,f=492)
    # vertices = []
    # normals = []
    # faces = []
    # with open(file_path) as f:
    #     while True:
    #         line = f.readline()
    #         if line == '':
    #             break
    #         items = line.strip().split()
    #         if len(items) == 0:
    #             continue
    #         if items[0] == 'v':
    #             vertices.append(list(map(float, items[1:])))
    #         elif items[0] == 'vn':
    #             normals.append(list(map(float, items[1:])))
    #         elif items[0] == 'f':
    #             faces.append(list(map(int, items[1:])))

    # 8.98s/10000time(v=298,f=492)
    with open(file_path) as f:
        lines = filter(lambda x: len(x) > 0,
                       [line.strip().split() for line in f.readlines()])
        vertices = [list(map(float, line[1:])) for line in lines if
                    line[0] == 'v']
        normals = [list(map(float, line[1:])) for line in lines if
                   line[0] == 'vn']

        def split_face_info(s):
            return [int(s) if s.isdigit() else None for s in s.split('/')]

        faces = [list(map(split_face_info, line[1:])) for line in lines if
                 line[0] == 'f']

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
