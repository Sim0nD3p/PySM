from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from elements.shelf.shelf import *


class ShelfContent(QWidget):


    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.list = QListWidget()
        self.main_vbox.addWidget(self.list)
        self.list.currentItemChanged.connect(self.handle_list_item_change)


        self.add_button = QPushButton('+')
        self.main_vbox.addWidget(self.add_button)

        self.setLayout(self.main_vbox)


    def display_blank(self):
        self.list.clear()
        self.add_button.setDisabled(True)

    def update_list_old(self, storage_list):
        """
        DEPRECIATED method in ShelfInspector
        :param storage_list:
        :return:
        """
        self.list.clear()
        for element in storage_list:
            item = QListWidgetItem(element.part_code, element)
            item.setData(0, element)
            print(item.data(0))
            print('element', element)
            self.list.addItem(item)



    def handle_list_item_change(self, item: QListWidgetItem):
        """
        Handle list item change for shelfContent
        :param item:
        :return:
        """
        print(item.text())
        print(item.data(1))



    def update_information(self, element):
        print('update shelf information, @shelfContent')
        if not element:
            pass
        elif issubclass(type(element), Shelf):
            self.parent_shelf = element

            self.add_button.setDisabled(False)



