from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QToolButton, QToolBar
from layout.central.storeOverview.physicalViewer.actions import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent


class StoreViewerControls(QToolBar):
    def __init__(self, store_viewer):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('toolbar')
        self.addAction(MoveUp(self, store_viewer))
        self.addAction(MoveDown(self, store_viewer))
        self.addAction(MoveLeft(self, store_viewer))
        self.addAction(MoveRight(self, store_viewer))
        self.addAction(ZoomOut(self, store_viewer))
        self.addAction(ZoomIn(self, store_viewer))

        self.new_drawing_action = NewDrawing(self, store_viewer)
        self.addAction(self.new_drawing_action)

        self.select_action = Select(self, store_viewer)
        self.addAction(self.select_action)
        # should use setBackgroundRole instead
        self.setStyleSheet('QWidget#toolbar{border:1px solid black; background-color:white}')

    def mousePressEvent(self, a0: QMouseEvent):
        print(a0.position())


