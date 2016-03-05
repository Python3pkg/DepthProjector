# coding=utf-8

import unittest
import pprint
from src.__io import read_obj

__author__ = 'kanairen'


class TestReadObj(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # face:v only
        self.file_path_0 = '../res/obj/0.obj'
        # normal exist & face:v//t
        self.file_path_1 = '../res/obj/1.obj'
        # non normal & face:v//t
        self.file_path_2 = '../res/obj/2.obj'

    def testReadObj(self):
        obj0 = read_obj(self.file_path_0)
        print obj0

        obj1 = read_obj(self.file_path_1)
        print obj1

        obj2 = read_obj(self.file_path_2)
        print obj2


if __name__ == '__main__':
    unittest.main()
