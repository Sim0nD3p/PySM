from OpenGL.raw.GL.VERSION.GL_1_0 import glClearColor, glClear, GL_COLOR_BUFFER_BIT
from PyQt6.QtCore import Qt, QRect, pyqtSignal
import math
import PyQt6
from backend.storeFloor import StoreFloor
from PyQt6.QtWidgets import *
from PyQt6 import QtOpenGLWidgets
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.storeViewerWidget.actions import *
from elements.store.storeObject import StoreObject
from backend.storeFloor import StoreFloor
from elements.store.dataClasses import *
from elements.elementsTypes import *
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
    mouse_release_signal = pyqtSignal(PyQt6.QtGui.QMouseEvent, name='name')
    new_rect_signal = pyqtSignal(ElementConstructorData, name='new_shape')
    selection_signal = pyqtSignal(StoreObject, name='selection')
    unselect_signal = pyqtSignal(name='unselect')


    def __init__(self):
        super().__init__()

        self.elements = []  # DEPRECIATED
        self.selected_element = None
        self.coord_scale_x = 8000
        self.x_offset = 0
        self.y_offset = 0

        # e = StoreViewerControls(store_viewer=self)

        tb = QToolBar(self)
        tb.setFloatable(True)
        tb.setMovable(True)
        tb.setAutoFillBackground(True)
        tb.setBackgroundRole(QPalette.ColorRole.AlternateBase)
        tb.addWidget(QLabel('test'))
        tb.addAction('action1')
        # TODO add zoom by scrolling

        self.setGeometry(0, 0, 100, 100)
        self.current_drawing = None
        self.mouse_pressed_position = QPointF(0, 0)
        self.mouse_action_type = ACTION_MOVE
        self.default_mouse_action_type = ACTION_MOVE

    def move_offset(self, x: int, y: int):
        """
        Move the store around by the offset specified
        ** might be scalable with zoom so that we always move by the same amount on screen

        :param x: int: x offset
        :param y: int: y offset
        :return:
        """
        self.x_offset += x
        self.y_offset += y

        self.repaint()

    def zoom_scalar(self, scalar):
        """
        Modify the self.current_scale_x with the scalar by addition
        :param scalar:
        :return:
        """
        self.coord_scale_x += scalar
        self.repaint()

    def get_logical_coordinates(self, mouse_event):
        """
        * USE INVERSE MATRIX INSTEAD
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

    def get_drawing_geometry(self, point1: QPointF, point2: QPointF):
        """
        Gets the geometry of the rectangle drawn from positions of pressed and released mouseEvent
        Calculate the x_position, y_position, length and width and return a constructorElement with the values
        :param point1: QPointF
        :param point2: QPointF
        :return: constructorElement
        """
        minx = min([point1.x(), point2.x()])
        maxx = max([point1.x(), point2.x()])
        miny = min([point1.y(), point2.y()])
        maxy = max([point1.y(), point2.y()])

        dx = maxx - minx
        dy = maxy - miny

        if abs(dx) >= abs(dy):
            length = dx
            width = dy
            x_position = minx
            y_position = -maxy
            angle = 0
        else:
            length = dy
            width = dx
            x_position = minx + width
            y_position = -maxy
            angle = 90

        element = ElementConstructorData(
            x_position=x_position,
            y_position=y_position,
            length=length,
            width=width,
            angle=angle,
            height=0,
            type=NONE,
            name=''
        )
        return element


    def wheelEvent(self, e: QWheelEvent):
        """
        TODO zomm in and out on wheel scroll
        :param e:
        :return:
        """
        pass


    def mousePressEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        x, y = self.get_logical_coordinates(a0)
        self.mouse_pressed_position = QPointF(x, y)
        if self.mouse_action_type is ACTION_DRAW:
            self.selected_element = None
            self.mouse_pressed_position = QPointF(x, y)

    def mouseMoveEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        """
        Triggered on mouseMove
        :param a0:
        :return:
        """
        x, y = self.get_logical_coordinates(a0)
        current_position = QPointF(x, y)

        if self.mouse_action_type is ACTION_DRAW:
            if type(self.mouse_pressed_position) is PyQt6.QtCore.QPointF:
                pp = QPainterPath()
                rect = QRectF(self.mouse_pressed_position, QPointF(x, y))
                pp.addRect(rect)
                self.current_drawing = pp
                self.repaint()
        elif self.mouse_pressed_position != current_position:
            dx = -int(current_position.x() - self.mouse_pressed_position.x())
            dy = -int(current_position.y() - self.mouse_pressed_position.y())
            self.move_offset(x=dx, y=dy)




    def mouseReleaseEvent(self, a0: PyQt6.QtGui.QMouseEvent):
        x, y = self.get_logical_coordinates(a0)
        mouse_released_position = QPointF(x, y)


        if self.mouse_action_type is ACTION_DRAW:
            print('MouseRelease on ACTION_DRAW')
            constructor = self.get_drawing_geometry(self.mouse_pressed_position, mouse_released_position)
            self.new_rect_signal.emit(constructor)
            self.mouse_pressed_position = None

        elif self.mouse_action_type is ACTION_SELECT:
            # self.selected_element = None
            # self.current_drawing = None
            for e in StoreFloor().objects:
                if issubclass(type(e), StoreObject):
                    if e.painter_path().contains(QPointF(x, y)):
                        self.selected_element = e
                        self.selection_signal.emit(self.selected_element)
            # if self.selected_element is None:
                # self.unselect_signal.emit()

            # set up logic for how to handle the switch to active drawing to null
        # elif self.mouse_action_type is ACTION_SELECT:
          #   print('repainte')

            # self.current_drawing = None
        self.paintGL()
        self.repaint()

    def draw_object(self, store_object: StoreObject):
        path = QPainterPath()
        vertices = store_object.vertices()

    def unselect_all(self):
        self.selected_element = None
        self.paintGL()
        self.repaint()



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
        # 2 first to move view, 2 last to set apsect ratio
        painter.setViewport(QRect(0, 0, self.width(), self.height()))

        pen = QPen()
        pen.setWidth(0)
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

        """
        We draw painterPaths
        """


        # self.elements is DEPRECIATED
        # for element in self.elements:
            # if type(element) is PyQt6.QtGui.QPainterPath:
                # painter.drawPath(element)

        for element in StoreFloor.objects:
            painter.drawPath(element.painter_path())
            # print('painting ', element.name)

        pen = QPen()
        pen.setWidth(0)
        pen.setColor(QColor(210, 213, 73))
        painter.setPen(pen)

        painter.setBrush(QColor(210, 213, 73))


        if self.selected_element is not None:
            painter.drawPath(self.selected_element.painter_path())

        if self.current_drawing:
            painter.drawPath(self.current_drawing)

        self.device_matrix = painter.deviceTransform()

        #OpenGL.GL.glDrawPixels(self.width(), self.height(), GL_BGRA, GL_UNSIGNED_BYTE, )
        # print(painter.worldTransform())


