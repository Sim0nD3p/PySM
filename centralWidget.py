from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
import sys


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(10, 10, 400, 400)
        self.setStyleSheet('background-color:blue')

        self.create_layout()

    def create_layout(self):
        hbox = QHBoxLayout()
        label = QLabel('This is label')
        hbox.addWidget(label)
        self.setLayout(hbox)