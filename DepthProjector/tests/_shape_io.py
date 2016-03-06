# coding=utf-8

import os
import unittest
from DepthProjector._shape_io import read_obj

__author__ = 'kanairen'


class TestReadObj(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # face:v only
        self.file_path_0 = os.path.join('.', 'res', 'obj', '0.obj')
        # non normal & face:v//t
        self.file_path_1 = os.path.join('.', 'res', 'obj', '1.obj')

    def testReadObj(self):
        obj0 = read_obj(self.file_path_0)
        print obj0

        obj1 = read_obj(self.file_path_1)
        print obj1


if __name__ == '__main__':
    unittest.main()
