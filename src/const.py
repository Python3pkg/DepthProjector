# coding: utf-8
"""
定数を保持するモジュール
定義時はArgumentParserに直接登録され
参照時はConstオブジェクトを介して参照される
"""

import argparse

_parser = argparse.ArgumentParser()


class _Const(object):
    """
    定数を保持するクラス
    """

    def __init__(self):
        self.__dict__['__consts'] = {}
        self.__dict__['__parsed'] = False

    def _parse_consts(self):
        result = _parser.parse_args()
        for name, value in vars(result).items():
            self.__dict__['__consts'][name] = value
        self.__dict__['__parsed'] = True

    def __getattr__(self, name):
        if not self.__dict__['__parsed']:
            self._parse_consts()
        if name not in self.__dict__['__consts']:
            raise AttributeError('get const:{}'.format(name))
        return self.__dict__['__consts'][name]

    def __setattr__(self, name, value):
        if not self.__dict__['__parsed']:
            self._parse_consts()
        if name in self.__dict__['__consts']:
            raise AttributeError('set const:{}'.format(name))
        self.__dict__['__consts'][name] = value


# 外部から使用されるConstオブジェクト
CONST = _Const()


def DEFINE(name, default_value, docstring, const_type):
    _parser.add_argument("--" + name, default=default_value, help=docstring,
                         type=const_type)
