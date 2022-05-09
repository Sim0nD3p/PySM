from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.central.storeOverview.panel.containerPanel.childrens.partSelector import *
from layout.central.storeOverview.panel.containerPanel.childrens.containerSelector import *
from layout.central.storeOverview.panel.containerPanel.childrens.containerOptionsWidget import *
from elements.shelf.shelf import *
from elements.ElementLogic.StorageObject import *

from layout.central.storeOverview.panel.containerPanel.childrens.originSelector import *


class SelectContainer(QWidget):
    """
    First tab in containerInspector
    interface to edit container part, location, number
    """


    def __init__(self):
        super().__init__()
        self.parent_shelf = None
        self.storage_object = None

        self.main_vbox = QVBoxLayout()

        # find perfect settings
        # self.setContentsMargins(0, 0, 0, 0)
        # self.main_vbox.setContentsMargins(5, 5, 5, 5)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)

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

        self.origin_selector = OriginSelector()
        self.main_vbox.addWidget(self.origin_selector)

        # container options
        self.container_options = ContainerOptionsWidget()
        self.container_options_sa = QScrollArea()
        self.container_options_sa.setMinimumWidth(200)
        self.container_options_sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.container_options_sa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.container_options_sa.setContentsMargins(5, 5, 5, 5)
        # self.container_options_sa.setHorizontalScrollBarPolicy()
        self.container_options_sa.setWidget(self.container_options)
        self.main_vbox.addWidget(self.container_options_sa)





        # self.main_vbox.addSpacing(10)

        self.setLayout(self.main_vbox)





    def update_ui(self, element: StorageObject):
        """
        Updates the UI elements that are not in child widgets
        :param element:
        :return: void
        """


        if hasattr(element, 'parent_shelf_id') and StoreFloor.get_shelf_by_id(element.parent_shelf_id):
            self.shelf_type_label.setText(StoreFloor.get_shelf_by_id(element.parent_shelf_id).type)
        else:
            self.shelf_type_label.setText('SHELF TYPE')

    def update_child_widgets(self, element: StorageObject):
        """
        Updates subwidgets with information, call display_content with storage_object as argument
        :param element:
        :return:
        """
        if element:
            self.update_ui(element)
            self.part_selector.display_content(element)
            self.container_selector.display_content(element)
            self.origin_selector.display_content(element)
            self.container_options.display_content(element)



    def get_container_types(self):
        """
        Get the containers types compatible with the shelf type
        :return:
        """
        shelf_type = self.parent_shelf.compatible
