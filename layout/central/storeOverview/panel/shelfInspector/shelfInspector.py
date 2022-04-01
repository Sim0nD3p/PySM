from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.components.contextInterface.shelfProperties import *


class ShelfInspector(QTabWidget):
    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()


        self.shelf_properties = ShelfProperties()
        self.addTab(self.shelf_properties, 'General')
        # self.main_vbox.addWidget(self.prop)

        # self.setLayout(self.main_vbox)

    def update_inspector_data(self, shelf):
        self.shelf_properties.update_properties(shelf)

    def display_blank(self):
        print('display blank')

    def update_child_information(self, element):
        self.shelf_properties.enable_all()
        print('update child infos shelf')
        if element is None:
            print('element None')
            self.display_blank()
            self.shelf_properties.element = None
            self.shelf_properties.disable_all()
        elif type(element) is ElementConstructorData:
            print('ElementConstructorData')
            self.shelf_properties.element = element
            self.shelf_properties.update_information(element)
        elif issubclass(type(element), Shelf):
            print('type shelf')
            self.shelf_properties.element = element
            self.shelf_properties.update_information(element)

