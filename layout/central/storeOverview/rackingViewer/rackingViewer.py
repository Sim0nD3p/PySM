from PyQt6 import QtOpenGLWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from elements.racking.racking import *
from OpenGL.GL import *
import math

from elements.shelf.shelf import Shelf


class RackingViewer(QtOpenGLWidgets.QOpenGLWidget):

    shelf_selection_signal = pyqtSignal(Shelf, name='shelf_select')
    def __init__(self):
        super().__init__()
        self.current_racking = Racking(name='sample', id=121212, x_position=0, y_position=0, width=100, length=400,
                                       angle=0, height=500)
        self.coord_scale_x = 100
        self.device_matrix = None


    def set_racking(self, racking: Racking):
        print('setting racking')
        self.current_racking = racking
        self.paintGL()

    def mousePressEvent(self, a0: QMouseEvent):
        x, y = self.get_logical_coordinates(a0)
        for shelf in self.current_racking.shelves:
            if self.shelf_path(shelf).contains(QPointF(x, y)):
                self.shelf_selection_signal.emit(shelf)




    def racking_path(self, racking: Racking):
        path = QPainterPath()
        path.moveTo(QPointF(0, 0))
        path.lineTo(QPointF(5, 0))
        path.lineTo(QPointF(5, racking.height()))
        path.lineTo(QPointF(0, racking.height()))

        path.moveTo(QPointF(self.coord_scale_x - 5, 0))
        path.lineTo(QPointF(self.coord_scale_x, 0))
        path.lineTo(QPointF(self.coord_scale_x, racking.height()))
        path.lineTo(QPointF(self.coord_scale_x - 5, racking.height()))
        path.lineTo(QPointF(self.coord_scale_x - 5, 0))

        return path

    def shelf_path(self, shelf: Shelf):
        path = QPainterPath()
        path.moveTo(QPointF(5, shelf.base_height))
        path.lineTo(QPointF(5, shelf.base_height + shelf.height()))
        path.lineTo(QPointF(self.coord_scale_x - 5, shelf.base_height + shelf.height()))
        path.lineTo(QPointF(self.coord_scale_x - 5, shelf.base_height))
        path.lineTo(QPointF(5, shelf.base_height))

        return path


    def get_logical_coordinates(self, mouse_event):
        if self.device_matrix:
            horizontal_translation = self.device_matrix.m31()
            horizontal_scale = self.device_matrix.m11()
            vertical_translation = self.device_matrix.m32()
            vertical_scale = self.device_matrix.m22()

            logical_x = (mouse_event.position().x() - horizontal_translation) / horizontal_scale
            logical_y = (mouse_event.position().y() - vertical_translation) / vertical_scale

            return logical_x, logical_y


    def paintGL(self):
        print('paintGL')
        painter = QPainter(self)
        painter.setViewport(QRect(0, 0, self.width(), self.height()))

        glClearColor(1, 0.5, 1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor(102, 102, 0))
        painter.setPen(pen)
        painter.setBrush(QColor(102, 102, 109))

        coord_scale_x = 500
        coord_scale_y = math.floor(self.height() / self.width()) * coord_scale_x
        painter.setWindow(0, 0, coord_scale_x, coord_scale_y)


        if self.current_racking:
            self.coord_scale_x = self.current_racking.length()
            coord_scale_y = self.current_racking.height()
            self.coord_scale_x = math.floor(self.width() / self.height() * coord_scale_y)
            print(self.coord_scale_x, coord_scale_y)
            painter.setWindow(0, 0, self.coord_scale_x, coord_scale_y)
            painter.drawRect(QRect(0, 0, 50, 50))

            painter.drawPath(self.racking_path(self.current_racking))
            for shelf in self.current_racking.shelves:
                painter.drawPath(self.shelf_path(shelf))

        self.device_matrix = painter.deviceTransform()

