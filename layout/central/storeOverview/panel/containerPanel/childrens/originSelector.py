from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from backend.storeFloor import *

from elements.ElementLogic.StorageObject import StorageObject


class OriginSelector(QWidget):
    origin_change_signal = pyqtSignal(int, int, name='origin_change')

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.x_pos = 0
        self.y_pos = 0

        title_label = QLabel('Origine')
        self.grid.addWidget(title_label, 1, 1, 1, 4)

        x_label = QLabel('x')
        self.x_sp = QSpinBox()
        self.x_sp.valueChanged.connect(self.handle_x_change)
        self.grid.addWidget(x_label, 2, 1, 1, 1)
        self.grid.addWidget(self.x_sp, 2, 2, 2, 2)

        y_label = QLabel('y')
        self.y_sp = QSpinBox()
        self.y_sp.valueChanged.connect(self.handle_y_change)
        self.grid.addWidget(y_label, 2, 5, 1, 1)
        self.grid.addWidget(self.y_sp, 2, 6, 2, 2)

        self.setLayout(self.grid)

    def get_origin(self):
        """
        Returns list of [x, y] of the selected values for the origin coordinate
        :return: list[int, int]
        """
        return [self.x_sp.value(), self.y_sp.value()]

    def handle_x_change(self, x):
        """
        Sets the value of x position
        :param x:
        :return:
        """
        self.x_pos = x
        self.update_ui()

    def handle_y_change(self, y):
        """
        Sets the value of y position
        :param y:
        :return:
        """
        self.y_pos = y
        self.update_ui()

    def update_ui(self):
        self.x_sp.setValue(int(self.x_pos))
        self.y_sp.setValue(int(self.y_pos))
        self.origin_change_signal.emit(self.x_pos, self.y_pos)


    def handle_origin_change_old(self):
        """
        Emits signal of the origin value
        :return:
        """
        self.origin_change_signal.emit(self.x_pos, self.y_pos)

    def display_blank(self):
        self.x_sp.setValue(0)
        self.y_sp.setValue(0)
        self.x_sp.setDisabled(True)
        self.y_sp.setDisabled(True)

    def display_content(self, element: StorageObject):
        if element.container_instance():
            shelf_instance = StoreFloor.get_shelf_by_id(element.parent_shelf_id)
            if shelf_instance:
                self.x_sp.setMaximum(int(shelf_instance.length()))
                self.y_sp.setMaximum(int(shelf_instance.width()))

            self.y_pos = int(element.y_position())
            self.x_pos = int(element.x_position())
            self.update_ui()

        self.x_sp.setDisabled(False)
        self.y_sp.setDisabled(False)




