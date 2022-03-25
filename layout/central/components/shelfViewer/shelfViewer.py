from PyQt6.QtCore import QRect
import math
from PyQt6.QtWidgets import *
from PyQt6 import QtOpenGLWidgets
from PyQt6.QtGui import *
import numpy as np
from elements.elementsTypes import *
from OpenGL.GL import *
from elements.ElementLogic.dataClasses import *

from elements.shelf.shelf import Shelf
from elements.container.container import Container

container = Container(name='container_test', container_type=BIN, length=50, width=25, height=25, weight_capacity=30)
dummy_shelf = Shelf(name='test', shelf_length=400, shelf_width=200, shelf_height=10, element_type=BIN)
path = QPainterPath()
path.addRect(0, 0, 25, 25)

class ShelfViewer(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        print(dummy_shelf)

        self.current_shelf = dummy_shelf
        self.current_shelf.add_container(container, Position(container.width(), 0))

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
        pen.setWidth(1)
        pen.setColor(QColor(102, 102, 0))
        painter.setPen(pen)

        painter.setBrush(QColor(102, 102, 109))





        if not self.current_shelf:
            print('nothing to show')
            painter.drawPath(path)
        else:
            self.coord_scale_x = self.current_shelf.length()
            coord_scale_y = math.floor((self.height() / self.width()) * self.coord_scale_x)
            painter.setWindow(
                0, # int(-self.coord_scale_x/2),
                -self.current_shelf.width(), # int(-coord_scale_y/2)-50,
                self.coord_scale_x,
                coord_scale_y
            )
            painter.drawPath(self.current_shelf.painter_path)
            painter.setBrush(QColor(102, 80, 50))
            # painter.drawRect(10, -10, 25, -25)
            for container in self.current_shelf.containers:
                print(container)
                painter.drawPath(container.painter_path)
                print(container.vertices())



