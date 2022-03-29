from PyQt6.QtWidgets import QWidget, QToolButton, QWidgetAction
from PyQt6.QtGui import QAction, QShortcut, QKeySequence, QPainterPath, QIcon
from PyQt6.QtCore import Qt, QPointF, QRectF
from layout.settings.settings import Settings
from backend.storeFloor import *

ACTION_DRAW = 'DRAW_ACTION'
ACTION_MOVE = 'MOVE_ACTION'
ACTION_ZOOM = 'ZOOM_ACTION'
ACTION_SELECT = "ACTION_SELECT"


class MoveUp(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Haut', parent)
        self.store_viewer = store_viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Up))
        self.setIcon(QIcon('res/icons/north_black_24dp.svg'))
        self.triggered.connect(lambda: self.store_viewer.move_offset(0, -Settings().move_click_offset))


class MoveDown(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Bas', parent)
        self.store_viewer = store_viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Down))
        self.setIcon(QIcon('res/icons/south_black_24dp.svg'))
        self.triggered.connect(lambda: self.store_viewer.move_offset(0, Settings().move_click_offset))


class MoveLeft(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Gauche', parent)
        self.store_viewer = store_viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Left))
        self.setIcon(QIcon('res/icons/west_black_24dp.svg'))
        self.triggered.connect(lambda: self.store_viewer.move_offset(-Settings().move_click_offset, 0))


class MoveRight(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Droite', parent)
        self.store_viewer = store_viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Right))
        self.setIcon(QIcon('res/icons/east_black_24dp.svg'))
        self.triggered.connect(lambda: self.store_viewer.move_offset(Settings().move_click_offset, 0))


class ZoomOut(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Zoom out', parent)
        self.store_viewer = store_viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_O))
        self.setIcon(QIcon('res/icons/zoom_out_black_24dp.svg'))
        self.triggered.connect(lambda: self.store_viewer.zoom_scalar(Settings.zoom_click_offset))


class ZoomIn(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Zoom in', parent)
        self.store_viewer = store_viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_I))
        self.setIcon(QIcon('res/icons/zoom_in_black_24dp.svg'))
        self.triggered.connect(lambda: self.store_viewer.zoom_scalar(-Settings.zoom_click_offset))


class NewDrawing(QAction):
    def __init__(self, parent, store_viewer):
        super().__init__('Nouvel élément', parent)
        # TODO: auto uncheck toolButton
        self.store_viewer = store_viewer
        self.setCheckable(True)
        self.setShortcut(QKeySequence(Qt.Key.Key_N))
        self.setIcon(QIcon('res/icons/add_black_24dp.svg'))
        self.triggered.connect(self.set_viewer_mouse_action_type)

    def set_viewer_mouse_action_type(self):
        """
        Sets the viewer's mouse action type to drawing
        :return: void
        """
        self.store_viewer.mouse_action_type = ACTION_DRAW

class Select(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Sélectionner', parent)
        self.viewer = viewer
        self.setCheckable(True)
        self.setShortcut(QKeySequence(Qt.Key.Key_V))
        self.setIcon(QIcon('res/icons/search_black_24dp.svg'))
        self.triggered.connect(self.set_mouse_action_type)

    def set_mouse_action_type(self):
        """
        Sets the viewer's mouse action type to select
        :return: void
        """
        self.viewer.mouse_action_type = ACTION_SELECT

class Delete(QAction):
    def __init__(self, parent, viewer):
        super().__init__('Supprimer', parent)
        self.viewer = viewer
        self.setShortcut(QKeySequence(Qt.Key.Key_Delete))
        self.setIcon(QIcon('res/icons/delete_black_24dp.svg'))
        self.triggered.connect(self.delete_selected_object)

    def delete_selected_object(self):
        StoreFloor.objects.remove(self.viewer.selected_element)
        self.viewer.selected_element = None
        self.viewer.repaint()

class MoveItem(QAction):
    def __init__(self, parent, store_viewer, shelf_viewer):
        super().__init__('Déplacer', parent=parent)
        self.setShortcut(QKeySequence(Qt.Key.Key_M))
        self.setIcon(QIcon('res/icons/pan_tool_black_24dp.svg'))


















