import numpy as np
from math import cos, sin, radians as rad
"""
Racking need dimensions, position, name

"""
class Racking:
    def __init__(self, x_position, y_position, width, length, angle):
        """

        :param x_position: origin
        :param y_position: origin
        :param width:
        :param length:
        :param angle: angle between positive x axis and width from origin
        """
        self.angle = angle
        self.matrix = np.matrix([
            [x_position, y_position],
            [length, width]
        ])

    def vertices(self):
        """
        [[origin, bottom right],
        [top left, top right]]
        :return:
        """
        flat = self.matrix.flatten().transpose()
        angle = self.angle
        transformation = np.matrix([
            [1, 0, 0, 0],   # x1
            [0, -1, 0, 0],   # y1
            [1, 0, cos(rad(angle)), 0],     # x2
            [0, -1, -sin(rad(angle)), 0],     # y2
            [1, 0, cos(rad(angle)), -sin(rad(angle))],  # x3
            [0, -1, -sin(rad(angle)), -cos(rad(angle))],   # y3
            [1, 0, 0, -sin(rad(angle))],    #x4
            [0, 1, 0, -cos(rad(angle))]  #y4
        ], dtype='float64')

        r = np.matmul(transformation, self.matrix.flatten().transpose(), dtype='float64')
        r = r.reshape(4, 2)

        return r


    def width(self):
        return self.matrix[1, 1]

    def length(self):
        return self.matrix[0, 1]

    def x_position(self):
        return self.matrix[0, 0]

    def y_position(self):
        return self.matrix[1, 0]


r = Racking(length=100, width=50, x_position=50, y_position=50, angle=90)
print(r.vertices())
