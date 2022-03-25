from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette

from layout.central.components.shelfViewer.shelfViewer import ShelfViewer

class ElementContent(QWidget):
    def __init__(self, submit_signal):
        super().__init__()
        self.submit_signal = submit_signal
        self.main_vbox = QVBoxLayout()
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.input_elements = []


        test = ShelfViewer()
        vbox = QVBoxLayout()
        vbox.addWidget(test)
        self.setLayout(vbox)

