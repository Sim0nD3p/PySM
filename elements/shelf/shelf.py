from layout.settings.settings import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import numpy as np

"""
Multiple shelves style:
- flat
"""
content_height = 0
net_height = Settings.default_shelf_net_height
x_position = 0
y_position = 0


class Shelf:
    """
    Parent class for shelf
    What should shelf do exactly

    about position: shelf have x and y positions (usually 0, 0), about where they are placed on racking\
    with origin in bottom left corner

    """
    def __init__(self, name, element_type, shelf_length, shelf_width, shelf_height):
        self.name = name
        self.type = element_type
        self.geometry_matrix = np.array([
            [shelf_length, shelf_width],
            [x_position, y_position],
            [shelf_height, net_height]
        ])
        self.painter_path = self.update_painter_path()
        self.content = []

    def length(self):
        """
        Length
        :return: length
        """
        return self.geometry_matrix[0, 0]

    def width(self):
        """
        Width
        :return: width
        """
        return self.geometry_matrix[0, 1]

    def vertices(self):
        """
        Gets vertices of the shelf with bottom left corner at (0, 0)
        :return:
        """
        geometry = np.resize(self.geometry_matrix, (4, 1))
        transformation = np.array([
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 1]
        ])
        vertices = np.matmul(transformation, geometry)
        return vertices.reshape(4, 2)

    def update_painter_path(self):
        """
        Vertices of the shelf (4 corners)
        :return:
        """
        path = QPainterPath()
        vertices = self.vertices()
        for i in range(0, len(vertices)):
            if i == 0:
                path.moveTo(QPointF(vertices[0, 0], vertices[0, 1]))
            else:
                path.lineTo(QPointF(vertices[i, 0], vertices[i, 1]))

        path.lineTo(QPointF(vertices[0, 0], vertices[0, 1]))

        return path





