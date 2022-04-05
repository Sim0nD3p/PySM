from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from elements.elementsTypes import *
from elements.container.container import *


class ContainerPanel(QWidget):
    """
    TODO PANEL MIGHT BE PARENT CLASS (show, hide, submit signal, cancel signal)
    """
    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.main_vbox.addWidget(QLabel('label test'))

        self.show_panel(300)
        self.setLayout(self.main_vbox)

    def show_panel(self, width):
        """
        Shows panel by setting minimum and maximum width to given width
        :param width: int
        :return: void
        """
        if not width:
            width = 250
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    def hide_panel(self):
        """
        Hides panel by setting width to 0
        :return:
        """
        self.setMaximumWidth(0)
        self.setMinimumWidth(0)
