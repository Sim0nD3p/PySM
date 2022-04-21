from dataclasses import dataclass
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.settings.settings import *
from math import *
from math import radians as rad
import numpy as np


@dataclass
class Position:
    x_position: float
    y_position: float

    def int_x(self):
        return int(self.x_position)

    def int_y(self):
        return int(self.y_position)


class Geometry:
    def __init__(self, length: float, width: float, x_position: float, y_position: float, angle: float, height: float):
        self.geometry = np.array([
            [length, width],
            [x_position, y_position],
            [angle, height]
        ])
        self.painter_path = self.update_painter_path()


    def x_position(self):
        """
        x_position: horizontal position of the bottom-left corner would the rectangle be horizontal
        :return: x_position
        """
        return self.geometry[1, 0]

    def set_x_position(self, x_position: float):
        """
        See x_position, sets the value for x_position in geometry_matrix and updates painterPath
        :param x_position: x_position
        :return: void
        """
        self.geometry[1, 0] = x_position
        self.update_painter_path()

    def y_position(self):
        """
        y_position: vertical position of the bottom-left corner would the rectangle be horizontal
        :return: y_position
        """
        return self.geometry[1, 1]

    def set_y_position(self, y_position: float):
        """
        See y_position, sets the value for y_position in geometry_matrix and updates painterPath
        :param y_position: y_position
        :return: void
        """
        self.geometry[1, 1] = y_position
        self.update_painter_path()

    def length(self):
        """
        length: length of the longest side of the rectangle
        :return: length
        """
        return self.geometry[0, 0]

    def set_length(self, length: float):
        """
        See length, sets the value for length in geometry_matrix and updates painterPath
        :param length: length
        :return: void
        """
        if length > 0:
            self.geometry[0, 0] = length
            self.update_painter_path()
        else:
            print('error length should be > 0')

    def width(self):
        """
        width: length of the shortest side of the rectangle
        :return: width
        """
        return self.geometry[0, 1]

    def set_width(self, width: float):
        """
        See width, sets the value for width and updates painterPath
        :param width: width
        :return: void
        """
        if width > 0:
            self.geometry[0, 1] = width
            self.update_painter_path()
        else:
            print('error width should be > 0')

    def angle(self):
        """
        angle: angle in degrees between the x axis and the longest side of the rectangle of the bottom, would be 0 if the
        rectangle if horizontal
        :return: angle (degrees)
        """
        return self.geometry[2, 0]

    def set_angle(self, angle: float):
        """
        See angle, sets the value for angle and updates painterPath
        :param angle: angle (degrees)
        :return: void
        """
        self.geometry[2, 0] = angle
        self.update_painter_path()

    def height(self):
        """
        height: total height of the object
        :return: height
        """
        return self.geometry[2, 1]

    def set_height(self, height: float):
        """
        See height, sets the value for height and updates painterPath
        :param height:
        :return:
        """
        if height <= Settings.store_object_max_height:
            self.geometry[2, 1] = height
            self.update_painter_path()
        else:
            print('error, height given is over the limit')

    def update_painter_path(self):
        """
        Updates the painterPath of the storeObject
        :return:
        """
        path = QPainterPath()
        vertices = self.vertices()

        for i in range(0, len(vertices)):
            if i == 0:
                path.moveTo(QPointF(vertices[i, 0], vertices[i, 1]))
            else:
                path.lineTo(QPointF(vertices[i, 0], vertices[i, 1]))

        path.lineTo(QPointF(vertices[0, 0], vertices[0, 1]))
        path.addEllipse(QPointF(vertices[0, 0], vertices[0, 1]), 0.5, 0.5)
        # path.addRect(10, -10, 25, -25)
        # print('path', path)
        self.painter_path = path
        return path

    def vertices(self):
        """
        :return: vertices of the StoreObject (np.matrix 4x2)
        """
        # TODO add adjustement for angle so that bottom left is always origin?
        angle = self.geometry[2, 0]
        transformation = np.array([
            [0, 0, 1, 0],   # x1
            [0, 0, 0, -1],   # y1
            [cos(rad(angle)), 0, 1, 0],     # x2
            [-sin(rad(angle)), 0, 0, -1],     # y2
            [cos(rad(angle)), -sin(rad(angle)), 1, 0],  # x3
            [-sin(rad(angle)), -cos(rad(angle)), 0, -1],   # y3
            [0, -sin(rad(angle)), 1, 0],    # x4
            [0, -cos(rad(angle)), 0, -1]  # y4
        ], dtype='float64')

        vertices = np.matmul(transformation, np.resize(self.geometry, (4, 1)), dtype='float64')
        vertices = vertices.reshape(4, 2)
        return vertices
