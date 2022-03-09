import sys
import random
from threading import Timer
import OpenGL.GL
import OpenGL.arrays.ctypesparameters
import glfw
from PyQt6.QtCore import Qt, QSize, QRect, QPoint
import math
import PyQt6
from PyQt6.QtCore import Qt
from PySide2.QtWidgets import QOpenGLWidget
from PyQt6.QtOpenGL import QOpenGLPaintDevice, QOpenGLWindow
from PyQt6 import QtOpenGL, QtCore
from PyQt6 import QtOpenGLWidgets
import numpy as np
from PyQt6.QtCore import Qt
from OpenGL.arrays import vbo
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen, QPixmap, QPainterPath, QPaintDevice, QOpenGLContext
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen, QPainterPath, QMouseEvent
from OpenGL.GL import *
from layout.central.storeOverview.physicalViewer.actions import *
# https://nrotella.github.io/journal/first-steps-python-qt-opengl.html#pyopengl

# solution is QOpenGLWidget
# https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtopenglwidgets/qopenglwidget.html?highlight=qopenglwidget#QOpenGLWidget
# uses OpenGL in a Qt widget

class Rect(QPainterPath):
    def __init__(self):
        super().__init__()
        self.addRect(20, 20, 60, 60)




class StoreTopVisualizer(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.coord_scale_x = 100
        self.x_offset = 0
        self.y_offset = 0
        # self.mousePressed = QMouseEvent('MouseButtonPressed')
        self.current_drawing = None

    def get_logical_coordinates(self, mouse_event):
        """
        Gets the logical coordinates of the mouse from mouseEvent
        :param mouse_event: PyQt6.QtGui.QMouseEvent
        :return: (x, y) logical coordinates
        """
        if self.device_matrix:
            horizontal_translation = self.device_matrix.m31()
            horizontal_scale = self.device_matrix.m11()
            vertical_translation = self.device_matrix.m32()
            vertical_scale = self.device_matrix.m22()

            logical_x = (mouse_event.position().x() - horizontal_translation) / horizontal_scale
            logical_y = (mouse_event.position().y() - vertical_translation) / vertical_scale

            return logical_x, logical_y

    def mousePressEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        print('mouse pressed')
        ne = NewDrawing(self)

        print(ne.isChecked())

        print(ne.painter_active)

        x, y = self.get_logical_coordinates(a0)
        dr = DrawingRectangle(self)
        if dr.drawing_active:
            # print('starting points', math.ceil(x), math.ceil(y))
            dr.set_starting_point(math.ceil(x), math.ceil(y))

    def mouseMoveEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        print('move')
        dr = DrawingRectangle(self)
        if dr.drawing_active:
            x, y = self.get_logical_coordinates(a0)
            path = dr.create_currently_drawn_rectangle(math.ceil(x), math.ceil(y))
            self.current_drawing = path
            self.paintGL()
            self.repaint()

    def mouseReleaseEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        print('release')




    def draw_rect(self):
        rect = QPainterPath()
        rect.addRect(0, 0, 10, 10)
        self.elements.append(rect)
        self.paintGL()


    def move_offset(self, x: int, y: int):
        """
        Move the store around by the offset specified
        ** might be scalable with zoom so that we always move by the same amount on screen

        :param x: int: x offset
        :param y: int: y offset
        :return:
        """
        print('move by ', x, y)
        self.x_offset += x
        self.y_offset += y

        self.paintGL()
        self.repaint()  # eliminate lag

    def zoom_scalar(self, scalar):
        """
        Modify the self.current_scale_x with the scalar by addition
        :param scalar:
        :return:
        """
        print('should setup logic for zoom')
        self.coord_scale_x += scalar
        self.paintGL()
        self.repaint()


    def move_vp(self):
        self.x_offset = self.x_offset + 10
        self.paintGL()


    def initializeGL(self):
        # we can start to use OpenGL context
        print('initialize GL')

        # print(painter.device())



    def resizeGL(self, width: int, height: int):
        print('resize GL')


    def paintEvent(self, e: PyQt6.QtGui.QPaintEvent):
        print('fdsfs')
    def paintGL(self):
        # called on resize
        print('paint GL')
        # print('size', self.height(), self.width())

        # setting background color directly on the OpenGL window

        painter = QPainter(self)
        print(self.x_offset, self.y_offset)


        coord_scale_y = math.floor((self.height() / self.width()) * self.coord_scale_x)
        painter.setWindow(
            -self.coord_scale_x / 2 + self.x_offset,
            -coord_scale_y / 2 + self.y_offset,
            self.coord_scale_x,
            coord_scale_y
        )

        # sets the coordinates system
        # TODO: add aspect ratio handling from widget source
        # painter.setWindow(QRect(-20, -20, 40, 40))
        # 652, 513
        # 2 first to move view, 2 last to set apsect ratio
        painter.setViewport(QRect(0, 0, self.width(), self.height()))


        # vprint(painter.viewport())
        # rect = Rect()


        pen = QPen()
        pen.setWidth(0.5)
        pen.setColor(QColor(102, 102, 109))

        print('pen', pen)
        painter.setPen(pen)
        painter.setBrush(QColor(102, 102, 109))

        # print('window', painter.window())
        # print('viewport', painter.viewport())
        painter.eraseRect(
            -self.coord_scale_x/2,
            -coord_scale_y/2,
            self.coord_scale_x,
            coord_scale_y)

        glClearColor(1, 1, 1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)



        for element in self.elements:
            if type(element) is PyQt6.QtGui.QPainterPath:
                print('eme')
                painter.drawPath(element)

        if self.current_drawing:
            print('drawing current')
            painter.drawPath(self.current_drawing)

        self.device_matrix = painter.deviceTransform()

        #OpenGL.GL.glDrawPixels(self.width(), self.height(), GL_BGRA, GL_UNSIGNED_BYTE, )
        # print(painter.worldTransform())


