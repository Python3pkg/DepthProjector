# coding=utf-8

import unittest
from src._shape import Shape, Obj

__author__ = 'kanairen'


class TestShape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "{}:setUpClass".format(cls.__name__)

    def setUp(self):
        print "{}:setUp".format(self.__class__.__name__)
        vertices = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.shape = Shape(vertices)
        self.first_shape = Shape(vertices)
        self.second_shape = Shape(vertices)
        self.third_shape = Shape(vertices)
        self.forth_shape = Shape(vertices)

    def test_center(self):
        print "{}:test_center".format(self.__class__.__name__)
        self.shape.center()
        self.shape.vertices = None
        self.shape.center()

    def test_normal(self):
        print "{}:test_center".format(self.__class__.__name__)
        self.shape.normal()

    def test_rotate(self):
        print "{}:test_rotate".format(self.__class__.__name__)

        first_angle = (90, 0, 0)
        self.first_shape.rotate(first_angle)
        print "test1{} :\n {}".format(first_angle, self.first_shape.vertices)

        second_angle = (0, 90, 0)
        self.second_shape.rotate(second_angle)
        print "test2{} :\n {}".format(second_angle, self.second_shape.vertices)

        third_angle = (0, 0, 90)
        self.third_shape.rotate(third_angle)
        print "test3{} :\n {}".format(third_angle, self.third_shape.vertices)

        forth_angle = (10, 20, 30)
        self.forth_shape.rotate(forth_angle)
        print "test4{} :\n {}".format(forth_angle, self.forth_shape.vertices)


class TestObj(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "{}:setUpClass".format(cls.__name__)

    def setUp(self):
        print "{}:setUp".format(self.__class__.__name__)
        vertices = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        normals = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        faces = [1, 2, 3]
        colors = [[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]]
        self.obj = Obj(vertices, normals, faces, colors)

    def test_center(self):
        print "{}:test_center".format(self.__class__.__name__)
        self.obj.center()


if __name__ == '__main__':
    unittest.main()
