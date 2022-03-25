from PyQt6.QtCore import QRect
import math
from PyQt6.QtWidgets import *
from PyQt6 import QtOpenGLWidgets
from PyQt6.QtGui import *
import numpy as np
from elements.elementsTypes import *
from OpenGL.GL import *

from elements.shelf.shelf import Shelf

dummy_shelf = Shelf(name='test', shelf_length=400, shelf_width=200, shelf_height=10, element_type=BIN)
path = QPainterPath()
path.addRect(0, 0, 25, 25)

class ShelfViewer(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        print(dummy_shelf)

        self.current_shelf = dummy_shelf

        self.coord_scale_x = 100
        self.x_offset = 0
        self.y_offset = 0

    def paintGL(self):
        painter = QPainter(self)
        coord_scale_y = math.floor((self.height() / self.width()) * self.coord_scale_x)

        painter.setWindow(
            int(-self.coord_scale_x / 2 + self.x_offset),
            int(-coord_scale_y / 2 + self.y_offset),
            self.coord_scale_x,
            coord_scale_y
        )

        painter.setViewport(QRect(0, 0, self.width(), self.height()))

        painter.eraseRect(
            int(-self.coord_scale_x / 2),
            int(-coord_scale_y / 2),
            self.coord_scale_x,
            coord_scale_y
        )

        glClearColor(1, 0.5, 1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        pen = QPen()
        pen.setWidth(0)
        pen.setColor(QColor(102, 102, 109))
        painter.setPen(pen)

        painter.setBrush(QColor(102, 102, 109))





        if not self.current_shelf:
            print('nothing to show')
            painter.drawPath(path)
        else:
            coord_scale_y = math.floor((self.height() / self.width()) * self.current_shelf.length())
            painter.setWindow(-10, -10, self.current_shelf.length() + 20, coord_scale_y)
            print('should draw shelf')
            print(self.current_shelf.vertices())
            painter.drawPath(self.current_shelf.painter_path)



