import numpy as np
from math import sin, cos, radians as rad

class StoreObject:
    """
    Parent class for all rectanglar store objects that have dimensions, position
    """
    def __init__(self, x_position, y_position, length, width, height, angle, element_type):
        self.geometry_matrix = np.matrix([
            [x_position, y_position],
            [length, width],
            [angle, height]
        ], dtype='float64')
        self.type = type

    def x_position(self):
        return self.geometry_matrix[0, 0]

    def y_position(self):
        return self.geometry_matrix[0, 1]

    def length(self):
        return self.geometry_matrix[1, 0]

    def width(self):
        return self.geometry_matrix[1, 1]

    def angle(self):
        return self.geometry_matrix[2, 0]

    def height(self):
        return self.geometry_matrix[2, 1]




    def vertices(self):
        """
        :return: vertices of the StoreObject (np.matrix 4x2)
        """
        angle = self.geometry_matrix[2, 0]
        transformation = np.matrix([
            [1, 0, 0, 0],   # x1
            [0, -1, 0, 0],   # y1
            [1, 0, cos(rad(angle)), 0],     # x2
            [0, -1, -sin(rad(angle)), 0],     # y2
            [1, 0, cos(rad(angle)), -sin(rad(angle))],  # x3
            [0, -1, -sin(rad(angle)), -cos(rad(angle))],   # y3
            [1, 0, 0, -sin(rad(angle))],    # x4
            [0, 1, 0, -cos(rad(angle))]  # y4
        ], dtype='float64')

        vertices = np.matmul(transformation, np.resize(self.geometry_matrix, (4, 1)), dtype='float64')
        vertices = vertices.reshape(4, 2)
        return vertices
