from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class ShelfContent(QWidget):
    new_container_signal = pyqtSignal(name='new_container')

    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.list = QListWidget()
        self.main_vbox.addWidget(self.list)


        self.add_button = QPushButton('+')
        self.add_button.clicked.connect(self.handle_add_button)
        self.main_vbox.addWidget(self.add_button)

        self.setLayout(self.main_vbox)

    def handle_add_button(self):
        """
        Emits new container signal
        :return:
        """
        self.new_container_signal.emit()

    def display_blank(self):
        self.list.clear()
        self.add_button.setDisabled(True)

