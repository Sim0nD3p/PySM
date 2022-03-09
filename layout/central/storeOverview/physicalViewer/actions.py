from PyQt6.QtWidgets import QWidget, QToolButton, QWidgetAction
from PyQt6.QtGui import QAction, QShortcut, QKeySequence, QPainterPath, QIcon
from PyQt6.QtCore import Qt, QPointF, QRectF
from layout.settings.settings import Settings


class MoveUp(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Haut', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Up))
        self.setIcon(QIcon('res/icons/north_black_24dp.svg'))
        self.triggered.connect(lambda: self.viewer.move_offset(0, -Settings().move_click_offset))



class MoveDown(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Bas', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Down))
        self.setIcon(QIcon('res/icons/south_black_24dp.svg'))
        self.triggered.connect(lambda: self.viewer.move_offset(0, Settings().move_click_offset))


class MoveLeft(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Gauche', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Left))
        self.setIcon(QIcon('res/icons/west_black_24dp.svg'))
        self.triggered.connect(lambda: self.viewer.move_offset(-Settings().move_click_offset, 0))


class MoveRight(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Droite', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Right))
        self.setIcon(QIcon('res/icons/east_black_24dp.svg'))
        self.triggered.connect(lambda: self.viewer.move_offset(Settings().move_click_offset, 0))


class ZoomOut(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Zoom out', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_O))
        self.setIcon(QIcon('res/icons/zoom_out_black_24dp.svg'))
        self.triggered.connect(lambda: self.viewer.zoom_scalar(Settings.zoom_click_offset))


class ZoomIn(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Zoom in', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_I))
        self.setIcon(QIcon('res/icons/zoom_in_black_24dp.svg'))
        self.triggered.connect(lambda: self.viewer.zoom_scalar(-Settings.zoom_click_offset))

class NewDrawing(QAction):
    painter_active = False

    def __init__(self, parent):
        super().__init__('Nouvel élément', parent)
        self.setShortcut(QKeySequence(Qt.Key.Key_N))
        self.setIcon(QIcon('res/icons/add_black_24dp.svg'))
        self.setCheckable(True)









class DrawingRectangle(QAction):
    drawing_active = False
    starting_point = QPointF(0, 0)

    def __init__(self, parent):
        super().__init__('Dessiner rectangle', parent)
        self.setShortcut(QKeySequence(Qt.Key.Key_M))
        self.setIcon(QIcon('res/icons/add_black_24dp.svg'))
        self.setCheckable(True)

    @classmethod
    def set_drawing_state(cls, status):
        """
        Sets the status of drawing active | inactive (bool)
        :param status: bool
        :return: void
        """
        cls.drawing_active = status

    @classmethod
    def set_starting_point(cls, x, y):
        """
        Stores the logical coordinates of the starting point of the currently drawn rectangle
        :param x: logical coordinate x
        :param y: logical coordinate y
        :return: void
        """
        cls.starting_point = QPointF(x, y)

    @classmethod
    def create_currently_drawn_rectangle(cls, current_x, current_y):
        """
        Creates the currently drawn rectangle and returns painterPath
        :param current_x: logical coordinate x
        :param current_y: logical coordinate y
        :return: QPainterPath
        """
        final_point = QPointF(current_x, current_y)
        pp = QPainterPath()
        rect = QRectF(cls.starting_point, final_point)

        pp.addRect(rect)
        return pp











