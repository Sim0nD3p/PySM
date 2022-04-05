from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from elements.elementsTypes import *
from elements.shelf.shelf import *
from elements.shelf.flatShelf import *
from elements.store.dataClasses import ElementConstructorData


class ShelfProperties(QWidget):
    """
    Manage properties of shelf
    """
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
        self.type_cb.setPlaceholderText('Type')
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

        height_hb = QHBoxLayout()
        height_label = QLabel('Hauteur')
        self.height_sb = QSpinBox()
        self.input_elements.append(self.height_sb)
        self.height_sb.setMinimum(0)
        self.height_sb.setMaximum(9999)
        height_hb.addWidget(height_label)
        height_hb.addWidget(self.height_sb)
        self.main_vbox.addLayout(height_hb)


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

        self.main_vbox.addSpacing(200)

        self.set_constraints()


        self.setLayout(self.main_vbox)




    def update_information(self, element):
        """
        Calls the right method to display shelf properties
        :param element:
        :return:
        """
        if type(element) == ElementConstructorData:
            self.element = None
            self.display_from_element_constructor(element)
        elif issubclass(type(element), Shelf):
            self.element = element
            self.display_from_object(element)

    def display_from_object(self, element: Shelf):
        """
        Displays shelf information from shelf object
        :param element:
        :return:
        """
        self.name_le.setText(str(element.name))
        self.length_sb.setValue(element.length())
        self.width_sb.setValue(element.width())
        self.height_sb.setValue(element.height())
        self.y_pos_sb.setValue(element.y_position())
        self.x_pos_sb.setValue(element.x_position())
        self.type_cb.setCurrentIndex(self.type_cb.findData(type(element)))

    def display_from_element_constructor(self, element: ElementConstructorData):
        """
        Displays shelf information from ElementConstructorData, defaults values
        :param element: ElementConstructorData
        :return: void
        """
        print('display values')
        print(element)
        self.name_le.setText(str(element.name))
        self.length_sb.setValue(int(element.length))
        self.height_sb.setValue(int(element.height))
        self.width_sb.setValue(int(element.width))
        self.x_pos_sb.setValue(int(element.x_position))
        print('calisse')

    def modify_part(self):
        if issubclass(type(self.element), Shelf):
            self.element.set_height(self.height_sb.value())
            self.element.set_x_position(self.x_pos_sb.value())
            self.element.set_y_position(self.y_pos_sb.value())
            self.element.set_width(self.width_sb.value())
            self.element.set_length(self.length_sb.value())
            print(vars(self.element))

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




    def update_type_cb(self):
        """
        Updates the content of ComboBox for type
        :return:
        """
        self.type_cb.addItem('Flat', userData=FlatShelf)



