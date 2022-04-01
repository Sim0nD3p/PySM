from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from elements.elementsTypes import *
from elements.shelf.shelf import *
from elements.shelf.flatShelf import *
from elements.store.dataClasses import ElementConstructorData


class ShelfProperties(QWidget):
    def __init__(self):
        super().__init__()
        self.element = None     # current shelf
        self.input_elements = []

        self.main_vbox = QVBoxLayout()

        # name label
        name_label = QLabel('Nom:')
        self.name_le = QLineEdit()
        self.input_elements.append(self.name_le)
        name_hb = QHBoxLayout()
        name_hb.addWidget(name_label)
        name_hb.addWidget(self.name_le)
        self.main_vbox.addLayout(name_hb)

        # type
        type_label = QLabel('Type:')
        self.type_cb = QComboBox()
        self.input_elements.append(self.type_cb)
        self.update_type_cb()
        type_hb = QHBoxLayout()
        type_hb.addWidget(type_label)
        type_hb.addWidget(self.type_cb)
        self.main_vbox.addLayout(type_hb)

        # dimensions
        dim_hb = QHBoxLayout()
        length_label = QLabel('Longueur')
        self.length_sb = QSpinBox()
        self.input_elements.append(self.length_sb)
        self.length_sb.setMinimum(0)
        self.length_sb.setMaximum(9999)
        width_label = QLabel('Largeur')
        self.width_sb = QSpinBox()
        self.input_elements.append(self.width_sb)
        self.width_sb.setMinimum(0)
        self.width_sb.setMaximum(9999)
        dim_hb.addWidget(length_label)
        dim_hb.addWidget(self.length_sb)
        dim_hb.addWidget(width_label)
        dim_hb.addWidget(self.width_sb)
        self.main_vbox.addLayout(dim_hb)

        # position
        pos_hb = QHBoxLayout()
        x_pos_label = QLabel('Position x')
        self.x_pos_sb = QSpinBox()
        self.input_elements.append(self.x_pos_sb)
        self.x_pos_sb.setMaximum(9999)
        self.x_pos_sb.setMinimum(-9999)
        y_pos_label = QLabel('Position y')
        self.y_pos_sb = QSpinBox()
        self.input_elements.append(self.y_pos_sb)
        self.y_pos_sb.setMaximum(9999)
        self.y_pos_sb.setMinimum(-9999)
        pos_hb.addWidget(x_pos_label)
        pos_hb.addWidget(self.x_pos_sb)
        pos_hb.addWidget(y_pos_label)
        pos_hb.addWidget(self.y_pos_sb)
        self.main_vbox.addLayout(pos_hb)

        self.set_constraints()


        self.setLayout(self.main_vbox)


    def set_constraints(self):
        """
        Enables and disables spinBox to modify geometry data
        :return: void
        """
        excluded_types = [FlatShelf]
        if self.element:
            if type(self.element) not in excluded_types:
                self.length_sb.setDisabled(True)
                self.width_sb.setDisabled(True)
                self.x_pos_sb.setDisabled(True)
                self.y_pos_sb.setDisabled(True)
            else:
                self.length_sb.setDisabled(False)
                self.width_sb.setDisabled(False)
                self.x_pos_sb.setDisabled(False)
                self.y_pos_sb.setDisabled(False)

    def update_information(self, element):
        if type(element) == ElementConstructorData:
            self.diaplay_from_element_constructor(element)

    def diaplay_from_element_constructor(self, element: ElementConstructorData):
        print('display values')
        print(element)
        self.name_le.setText(str(element.name))
        self.length_sb.setValue(int(element.length))
        self.width_sb.setValue(int(element.width))
        self.x_pos_sb.setValue(int(element.x_position))
        print('calisse')

    def disable_all(self):
        """
        Sets setDisabled(True) for all input elements
        :return:
        """
        for element in self.input_elements:
            element.setDisabled(True)

    def enable_all(self):
        """
        Sets setDisabled(False) for all input elements
        :return:
        """
        for element in self.input_elements:
            element.setDisabled(False)




    def update_type_cb(self):
        """
        Updates the content of ComboBox for type
        :return:
        """
        self.type_cb.addItem('Flat', userData=FLAT_SHELF)


