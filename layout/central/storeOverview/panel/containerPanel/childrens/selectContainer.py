from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.central.storeOverview.panel.containerPanel.childrens.partSelector import *
from layout.central.storeOverview.panel.containerPanel.childrens.containerSelector import *
from layout.central.storeOverview.panel.containerPanel.childrens.containerOptions import *
from elements.shelf.shelf import *
from elements.ElementLogic.StorageObject import *


class SelectContainer(QWidget):
    """
    interface to edit container part, location, number
    """


    def __init__(self):
        super().__init__()
        self.parent_shelf = None
        self.storage_object = None

        self.main_vbox = QVBoxLayout()

        # shelf type
        hbox = QHBoxLayout()
        type_label = QLabel("Type d'étagère: ")
        self.shelf_type_label = QLabel('SHELF TYPE')
        font = QFont('Arial')
        font.setBold(True)
        self.shelf_type_label.setFont(font)
        hbox.addWidget(type_label)
        hbox.addWidget(self.shelf_type_label)
        self.main_vbox.addLayout(hbox)

        # part selector
        self.part_selector = PartSelector()
        self.main_vbox.addWidget(self.part_selector)

        # container selector
        self.container_selector = ContainerSelector()
        self.main_vbox.addWidget(self.container_selector)

        # container options
        self.container_options = ContainerOptions()
        self.container_options_sa = QScrollArea()
        self.container_options_sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.container_options_sa.setHorizontalScrollBarPolicy()
        self.container_options_sa.setWidget(self.container_options)
        self.main_vbox.addWidget(self.container_options_sa)





        self.main_vbox.addSpacing(10)




        self.setLayout(self.main_vbox)

    def update_ui(self, element: StorageObject):
        """
        Updates the UI elements that are not in child widgets
        :param element:
        :return: void
        """
        if StoreFloor.get_shelf_by_id(element.parent_shelf_id):
            shelf_type = StoreFloor.get_shelf_by_id(element.parent_shelf_id).type
            self.shelf_type_label.setText(shelf_type)
        else:
            self.shelf_type_label.setText('SHELF TYPE')



    def update_informations(self, element):
        """
        Updates child elements with info
        :param element:
        :return:
        """
        print('SelectContainer: receiving info on StoreObject')
        if issubclass(type(element), StorageObject):
            self.storage_object = element   # calling update on all child
            self.update_ui(element)
            self.container_selector.update_information(element)
            self.container_options.update_information(element)
            self.part_selector.update_completer()
            # print('all infos updated on selectContainer')
        elif not element:
            self.storage_object = None
            self.update_ui(None)
            self.container_selector.update_information(None)
            self.container_options.update_information(None)



    def get_container_types(self):
        """
        Get the containers types compatible with the shelf type
        :return:
        """
        shelf_type = self.parent_shelf.compatible
