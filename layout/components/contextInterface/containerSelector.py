from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from elements.elementsTypes import *


class ContainerSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()

        self.cont_type_cb = QComboBox()
        self.update_cont_type_cb()

        self.setLayout(self.main_vbox)

    def update_cont_type_cb(self):
        """
        draw containers types and data into comboBox
        :return:
        """
        self.cont_type_cb.addItem('Bin', userData=BIN)
        
