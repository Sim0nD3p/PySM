import numpy as np
from math import sin, cos, radians as rad
from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QPointF
from layout.settings.settings import Settings


class StoreObject:
    """
    Parent class for all rectanglar store objects that have dimensions, position
    should have painterPath directly implemented (isolated to the best we can)
    TODO: meaning of length and width when variable length/width
    """
    def __init__(self, name, id, x_position, y_position, length, width, height, angle, element_type):
        self.name = name
        self.id = id
        self.type = element_type
        self.geometry_matrix = np.array([
            [length, width],
            [x_position, y_position],
            [angle, height]
        ], dtype='float64')
        self.painter_path = self.update_painter_path()

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
        # print('path', path)
        self.painter_path = path
        return path

    def x_position(self):
        """
        x_position: horizontal position of the bottom-left corner would the rectangle be horizontal
        :return: x_position
        """
        return self.geometry_matrix[1, 0]

    def set_x_position(self, x_position: float):
        """
        See x_position, sets the value for x_position in geometry_matrix and updates painterPath
        :param x_position: x_position
        :return: void
        """
        self.geometry_matrix[1, 0] = x_position
        self.update_painter_path()

    def y_position(self):
        """
        y_position: vertical position of the bottom-left corner would the rectangle be horizontal
        :return: y_position
        """
        return self.geometry_matrix[1, 1]

    def set_y_position(self, y_position: float):
        """
        See y_position, sets the value for y_position in geometry_matrix and updates painterPath
        :param y_position: y_position
        :return: void
        """
        self.geometry_matrix[1, 1] = y_position
        self.update_painter_path()

    def length(self):
        """
        length: length of the longest side of the rectangle
        :return: length
        """
        return self.geometry_matrix[0, 0]

    def set_length(self, length: float):
        """
        See length, sets the value for length in geometry_matrix and updates painterPath
        :param length: length
        :return: void
        """
        if length > 0:
            self.geometry_matrix[0, 0] = length
            self.update_painter_path()
        else:
            print('error length should be > 0')

    def width(self):
        """
        width: length of the shortest side of the rectangle
        :return: width
        """
        return self.geometry_matrix[0, 1]

    def set_width(self, width: float):
        """
        See width, sets the value for width and updates painterPath
        :param width: width
        :return: void
        """
        print('setting width')
        print(width)
        if width > 0:
            self.geometry_matrix[0, 1] = width
            self.update_painter_path()
        else:
            print('error width should be > 0')

    def angle(self):
        """
        angle: angle in degrees between the x axis and the longest side of the rectangle of the bottom, would be 0 if the
        rectangle if horizontal
        :return: angle (degrees)
        """
        return self.geometry_matrix[2, 0]

    def set_angle(self, angle: float):
        """
        See angle, sets the value for angle and updates painterPath
        :param angle: angle (degrees)
        :return: void
        """
        self.geometry_matrix[2, 0] = angle
        self.update_painter_path()

    def height(self):
        """
        height: total height of the object
        :return: height
        """
        return self.geometry_matrix[2, 1]

    def set_height(self, height: float):
        """
        See height, sets the value for height and updates painterPath
        :param height:
        :return:
        """
        if height <= Settings.store_object_max_height:
            self.geometry_matrix[2, 1] = height
            self.update_painter_path()
        else:
            print('error, height given is over the limit')

    def vertices(self):
        """
        :return: vertices of the StoreObject (np.matrix 4x2)
        """
        angle = self.geometry_matrix[2, 0]
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

        vertices = np.matmul(transformation, np.resize(self.geometry_matrix, (4, 1)), dtype='float64')
        vertices = vertices.reshape(4, 2)
        return vertices

"""
transformation = np.array([
            [1, 0, 0, 0],   # x1
            [0, -1, 0, 0],   # y1
            [1, 0, cos(rad(angle)), 0],     # x2
            [0, -1, -sin(rad(angle)), 0],     # y2
            [1, 0, cos(rad(angle)), -sin(rad(angle))],  # x3
            [0, -1, -sin(rad(angle)), -cos(rad(angle))],   # y3
            [1, 0, 0, -sin(rad(angle))],    # x4
            [0, -1, 0, -cos(rad(angle))]  # y4
        ], dtype='float64')
"""

