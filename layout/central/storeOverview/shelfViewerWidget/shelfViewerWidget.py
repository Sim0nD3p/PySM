from PyQt6.QtWidgets import *
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *

class ShelfViewerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.setStyleSheet('background-color: red')
        self.shelf_visual = ShelfViewer()
        self.main_vbox.addWidget(self.shelf_visual)

        self.draw_layout()

    def draw_layout(self):
        self.setLayout(self.main_vbox)