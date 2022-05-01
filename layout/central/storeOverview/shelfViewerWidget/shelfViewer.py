from PyQt6.QtCore import *
from PyQt6.QtGui import *
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

container = Container(name='container_test', container_type=BIN, length=50, width=25, height=25, weight_capacity=30, net_weight=12)
dummy_shelf = Shelf(name='test', id=1010, shelf_length=400, shelf_width=200, shelf_height=10, x_position=0, y_position=0, type='hello')
path = QPainterPath()
path.addRect(0, 0, 25, 25)

class ShelfViewer(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.device_transform = None


        self.current_shelf = dummy_shelf
        # self.current_shelf.add_container(container, Position(0, 0))

        self.coord_scale_x = 100
        self.x_offset = 0
        self.y_offset = 0

    def mousePressEvent(self, a0: QMouseEvent):
        # print('eventPosition', a0.position().x(), a0.position().y())
        if self.device_transform and self.device_transform.isInvertible():
            x, y = self.device_transform.inverted()[0].map(a0.position().x(), a0.position().y())
            # print(x, y)
            drag = QDrag(self)

    def paint_shelf(self, shelf: Shelf):
        self.current_shelf = shelf
        self.paintGL()

    def paint_shelf_old(self):
        painter = QPainter()
        if issubclass(type(self.current_shelf), Shelf):
            for container in self.current_shelf.containers():
                print(container)
                painter.setBrush()
                painter.drawPath(container.painter_path())




    def paintGL(self):
        # print('paintGL')
        painter = QPainter(self)
        painter.setViewport(QRect(0, 0, self.width(), self.height()))
        """
        painter.eraseRect(
            int(-self.coord_scale_x / 2),
            int(-coord_scale_y / 2),
            self.coord_scale_x,
            coord_scale_y
        )
        """
        glClearColor(1, 0.5, 1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor(102, 102, 0))
        painter.setPen(pen)

        painter.setBrush(QColor(102, 102, 109))

        if not self.current_shelf:
            pass
            # print('nothing to show')
            # painter.drawPath(path)
        else:
            self.coord_scale_x = self.current_shelf.length()
            coord_scale_y = self.current_shelf.width()
            self.coord_scale_x = math.floor((self.width() / self.height()) * coord_scale_y)
            x_offset = 0
            y_offset = 0
            if painter.window().height() < self.current_shelf.width():
                coord_scale_y = self.current_shelf.width()
                self.coord_scale_x = math.floor((self.width() / self.height()) * coord_scale_y)
            x_offset = -math.floor((self.coord_scale_x - self.current_shelf.length()) / 2)
            if self.current_shelf.length() > self.coord_scale_x:
                self.coord_scale_x = self.current_shelf.length()
                coord_scale_y = math.floor((self.height() / self.width()) * self.coord_scale_x)
                x_offset = 0
                y_offset = math.floor((coord_scale_y - self.current_shelf.width()) / 2)
            painter.setWindow(
                0 + x_offset,
                -coord_scale_y + y_offset,
                self.coord_scale_x,
                coord_scale_y
            )
            painter.drawPath(self.current_shelf.painter_path())
            painter.setBrush(QColor(102, 80, 50))

            for container in self.current_shelf.containers():
                pen.setColor(QColor(0, 100, 0))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawPath(container.painter_path())




            # self.paint_shelf()

        if self.device_transform != painter.deviceTransform():   # sets transformation matrix
            self.device_transform = painter.deviceTransform()




