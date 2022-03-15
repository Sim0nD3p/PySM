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
from elements.racking.racking import Racking
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
        self.selected_elements = []
        self.coord_scale_x = 100
        self.rack = Racking(0, 0, 25, 50, 0)
        self.x_offset = 0
        self.y_offset = 0
        self.current_drawing = None
        self.mouse_pressed_position = None
        self.mouse_action_type = ACTION_MOVE
        self.default_mouse_action_type = ACTION_MOVE

        self.rect = None

    def get_logical_coordinates(self, mouse_event):
        """
        * USE INVERSE MATRIX INSTEAD? SEE LINEAR ALGEBRA CONCEPTS
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
        x, y = self.get_logical_coordinates(a0)

        if self.mouse_action_type is ACTION_SELECT:
            print('check for select')
            for e in self.elements:
                if e.contains(QPointF(x, y)):
                    if e not in self.selected_elements:
                        self.selected_elements.append(e)
                    print('found element')
                    self.paintGL()
                    self.repaint()

        elif self.mouse_action_type is ACTION_DRAW:
            self.mouse_pressed_position = QPointF(x, y)






    def mouseMoveEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        x, y = self.get_logical_coordinates(a0)
        if self.mouse_action_type is ACTION_DRAW:
            if type(self.mouse_pressed_position) is PyQt6.QtCore.QPointF:
                pp = QPainterPath()
                rect = QRectF(self.mouse_pressed_position, QPointF(x, y))
                pp.addRect(rect)
                self.current_drawing = pp
                self.paintGL()
                self.repaint()



    def mouseReleaseEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        print('release')
        super().mouseReleaseEvent(a0)
        if self.mouse_action_type is ACTION_DRAW:
            if self.current_drawing not in self.elements:
                self.elements.append(self.current_drawing)


            self.current_drawing = None
            self.mouse_pressed_position = None


        # self.mouse_action_type = self.default_mouse_action_type






    def draw_shape(self):
        # print('draw rect')
        re = Racking(x_position=0, y_position=0, width=25, length=50, angle=0)
        pp = QPainterPath()

        vertices = re.vertices()
        for vertex in vertices:
            pp.lineTo(QPointF(vertex[0, 0], vertex[0, 1]))
            print(vertices[0, 0])
        pp.lineTo(QPointF(vertices[0, 0], vertices[0, 1]))
        self.rect = pp
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


    def paintGL(self):

        painter = QPainter(self)
        coord_scale_y = math.floor((self.height() / self.width()) * self.coord_scale_x)
        painter.setWindow(
            -self.coord_scale_x / 2 + self.x_offset,
            -coord_scale_y / 2 + self.y_offset,
            self.coord_scale_x,
            coord_scale_y
        )

        # sets the coordinates system
        # TODO: add aspect ratio handling from widget source
        # 2 first to move view, 2 last to set apsect ratio
        painter.setViewport(QRect(0, 0, self.width(), self.height()))

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor(102, 102, 109))
        painter.setPen(pen)

        painter.setBrush(QColor(102, 102, 109))

        painter.eraseRect(
            -self.coord_scale_x/2,
            -coord_scale_y/2,
            self.coord_scale_x,
            coord_scale_y
        )
        # has to be after the eraseRect
        glClearColor(1, 1, 1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # self.draw_rect()
        if self.rect is not None:
            print('paint rect')
            painter.drawPath(self.rect)

        for element in self.elements:
            if type(element) is PyQt6.QtGui.QPainterPath:
                painter.drawPath(element)

        pen = QPen()
        pen.setWidth(0.5)
        pen.setColor(QColor(210, 213, 73))
        painter.setPen(pen)

        painter.setBrush(QColor(210, 213, 73))


        for selected_element in self.selected_elements:
            # painter.drawPath(selected_element)
            if type(selected_element) is PyQt6.QtGui.QPainterPath:
                print('should draw element')
                print(selected_element)
                painter.drawPath(selected_element)

        if self.current_drawing:
            painter.drawPath(self.current_drawing)

        self.device_matrix = painter.deviceTransform()

        #OpenGL.GL.glDrawPixels(self.width(), self.height(), GL_BGRA, GL_UNSIGNED_BYTE, )
        # print(painter.worldTransform())


