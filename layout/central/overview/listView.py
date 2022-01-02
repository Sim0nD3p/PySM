from PyQt6.QtWidgets import QListWidget, QLabel, QPushButton, QWidget, QHBoxLayout

class ListWidget(QWidget):
    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout()
        self.list = QListWidget()
        self.list.addItem('hello')
        hbox.addWidget(self.list)
        self.setLayout(hbox)

