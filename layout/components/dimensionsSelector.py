from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class DimensionSelector(QWidget):
    dimensions_change = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.main_hbox = QHBoxLayout()
        self.main_hbox.setContentsMargins(0, 0, 0, 0)
        self.spacing_size = 10
        self.input_elements = []

        width_la = QLabel('W')
        length_la = QLabel('L')
        height_la = QLabel('H')


        self.length_sp = QSpinBox()
        self.input_elements.append(self.length_sp)
        self.length_sp.valueChanged.connect(self.dimensions_change.emit)
        self.width_sp = QSpinBox()
        self.input_elements.append(self.width_sp)
        self.width_sp.valueChanged.connect(self.dimensions_change.emit)
        self.height_sp = QSpinBox()
        self.input_elements.append(self.height_sp)
        self.height_sp.valueChanged.connect(self.dimensions_change.emit)

        self.main_hbox.addWidget(length_la)
        self.main_hbox.addWidget(self.length_sp)
        self.main_hbox.addSpacing(self.spacing_size)
        self.main_hbox.addWidget(width_la)
        self.main_hbox.addWidget(self.width_sp)
        self.main_hbox.addSpacing(self.spacing_size)
        self.main_hbox.addWidget(height_la)
        self.main_hbox.addWidget(self.height_sp)

        self.setup_input()



        self.setLayout(self.main_hbox)

    def setup_input(self):
        for element in self.input_elements:
            element.setMaximum(9999)

    def width(self):
        return self.width_sp.value()

    def height(self):
        return self.height_sp.value()

    def length(self):
        return self.length_sp.value()

    def set_disabled(self, state: bool):
        for element in self.input_elements:
            element.setDisabled(state)

    def set_dimensions(self, length: int, width: int, height: int):
        """
        Sets the values for spinBox to the guiven ones
        :param length: int
        :param width: int
        :param height: int
        :return: void
        """
        self.length_sp.setValue(length)
        self.width_sp.setValue(width)
        self.height_sp.setValue(height)

    def enable_input(self):
        for element in self.input_elements:
            element.setDisabled(False)

    def display_blank(self):
        for element in self.input_elements:
            element.setValue(0)
            element.setDisabled(True)

