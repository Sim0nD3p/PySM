from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QToolButton, QToolBar
from layout.central.storeOverview.physicalViewer.actions import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent


class StoreViewerControls(QToolBar):
    def __init__(self, store_viewer):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.addAction(MoveUp(self, store_viewer))
        self.addAction(MoveDown(self, store_viewer))
        self.addAction(MoveLeft(self, store_viewer))
        self.addAction(MoveRight(self, store_viewer))
        self.addAction(ZoomOut(self, store_viewer))
        self.addAction(ZoomIn(self, store_viewer))


        self.new_drawing_action = NewDrawing(self)

        self.addAction(self.new_drawing_action)
        # self.setStyleSheet('background-color:red')

    def mousePressEvent(self, a0: QMouseEvent):
        print(a0.position())


