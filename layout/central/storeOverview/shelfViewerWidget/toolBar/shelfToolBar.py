from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.storeViewerWidget.actions import *


class ShelfToolBar(QToolBar):
    def __init__(self, shelf_viewer):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.addAction(MoveItem(self, shelf_viewer=shelf_viewer))
