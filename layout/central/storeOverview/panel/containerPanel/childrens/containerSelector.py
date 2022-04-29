from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from elements.shelf.shelf import *
from elements.shelf.flatShelf import *
from backend.ContainerCatalog import *
from layout.components.dimensionsSelector import *
from elements.ElementLogic.StorageObject import *
from backend.storeFloor import *


class ContainerSelector(QWidget):
    """
    Selects the container
    """
    container_change = pyqtSignal(Container, name='container_change')       # takes container Instance in argument

    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.container_instance = None

        # label container selector
        self.main_vbox.addSpacing(10)
        label_cont_select = QLabel('Choix contenant')
        self.main_vbox.addWidget(label_cont_select)

        # type contenant
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        type_label = QLabel('Type de contenant:')
        self.type_cb = QComboBox()
        hbox.addWidget(type_label)
        hbox.addWidget(self.type_cb)
        self.main_vbox.addLayout(hbox)

        # subtype contentant
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        cont_label = QLabel('Contenant: ')
        self.subtype_cb = QComboBox()
        hbox.addWidget(cont_label)
        hbox.addWidget(self.subtype_cb)
        self.main_vbox.addLayout(hbox)

        self.type_cb.currentIndexChanged.connect(self.handle_type_change)
        self.subtype_cb.currentIndexChanged.connect(self.handle_subtype_change)

        self.dimensions_selector = DimensionSelector()
        # self.dimensions_selector.dimensions_change.connect(self.handle_dimensions_change)
        self.main_vbox.addWidget(self.dimensions_selector)



        self.setLayout(self.main_vbox)


    def draw_type_cb(self, element: Shelf):
        """
        Draws the type combobox for compatible container fo a given shelving
        :param element: Shelf
        :return:
        """
        self.type_cb.clear()    # problem seems to be here, makes app crash, triggers valueChange
        # print('drawTypeCB')
        for container in element.compatible_containers:
            self.type_cb.addItem(container.display_type, container)


    def handle_type_change(self, type_cb_index):
        """
        Handles ComboBox for subtypes according to type selected in type comboBox
        :param type_cb_index: index of type ComboBox
        :return:
        """
        # print('handle type change')
        if type_cb_index != -1:
            container_type = self.type_cb.itemData(type_cb_index)
            subtypes = ContainerCatalog().get_containers(container_type=container_type)
            print('new container type')

            self.subtype_cb.clear()
            if len(subtypes) == 0:
                # New type of container is selected that doesnt have subtype, type is sent to storageObject for update
                container = ContainerCatalog.create_containers_from_type(container_type, 1)[0]     # container instance
                if self.container_instance:
                    container.set_length(self.container_instance.length())
                    container.set_width(self.container_instance.width())
                    container.set_height(self.container_instance.height())
                self.dimensions_selector.set_dimensions(
                    length=container.length(),
                    width=container.width(),
                    height=container.height()
                )
                self.container_change.emit(container)
                self.subtype_cb.setDisabled(True)
            else:
                self.subtype_cb.setDisabled(False)
                for subtype in subtypes:
                    self.subtype_cb.addItem(subtype.name, subtype)

    def handle_subtype_change(self, subtype_cb_index):
        # print('handle subtype change')

        if subtype_cb_index != -1:      # if we have valid subtype
            subtype = self.subtype_cb.itemData(subtype_cb_index)
            if issubclass(type(subtype), Container):
                self.dimensions_selector.setDisabled(True)

                self.dimensions_selector.set_dimensions(length=subtype.length(),
                                                        width=subtype.width(),
                                                        height=subtype.height()
                                                        )
                container = ContainerCatalog.create_containers(subtype, 1)[0]   # container instance
                self.container_change.emit(container)

        elif self.type_cb.currentIndex() != -1:     # if we have valid type
            self.dimensions_selector.set_dimensions(length=0,
                                                    width=0,
                                                    height=0
                                                    )
            self.dimensions_selector.setDisabled(False)


    def handle_dimensions_change_old(self):
        """
        Called when dimensions change signal is emitted from dimensions widget
        :return:
        """
        length = self.dimensions_selector.length()
        width = self.dimensions_selector.width()
        height = self.dimensions_selector.height()
        if self.type_cb.currentIndex() != -1:
            container = self.type_cb.itemData(self.type_cb.currentIndex())
            self.container_change.emit(container, length, width, height)



    def get_container_instance(self):
        """
        Returns an instance of the selected container with dimensions
        :return:
        """
        instance = None
        if self.type_cb.currentIndex() != -1:
            type_data = self.type_cb.itemData(self.type_cb.currentIndex())
            if len(ContainerCatalog.get_containers(type_data)) == 0:
                instance = ContainerCatalog.create_containers_from_type(type_data, 1)[0]    # main types stored as type
                # not instances
                instance.set_length(self.dimensions_selector.length())      # setting diemnsions
                instance.set_width(self.dimensions_selector.width())
                instance.set_height(self.dimensions_selector.height())
            elif self.subtype_cb.currentIndex() != -1:
                instance = self.subtype_cb.itemData(self.subtype_cb.currentIndex())     # subtypes stored as instances

        return instance


    def display_blank(self):
        """
        Display blank values for all input elements
        :return:
        """
        self.type_cb.clear()
        self.subtype_cb.clear()
        self.container_instance = None
        self.dimensions_selector.set_dimensions(0, 0, 0)

    def find_cb_index(self, cb: QComboBox, data):
        """
        Finds the index of cb that correspond the give data.
        Loops through all index and check if data matches. For subtypes, checks if it is the same container class and
        same dimensions
        :param cb: QComboBox
        :param data: Data to find
        :return:
        """
        index = -1
        for i in range(0, cb.count()):
            current_data = cb.itemData(i)
            if current_data == data:
                index = i
            elif issubclass(type(current_data), type(data)) and issubclass(type(current_data), Container):
                if data.length() == current_data.length() and data.width() == current_data.width() \
                        and data.height() == current_data.height():
                    index = i
        return index





    def display_content(self, content: StorageObject):
        """
        Main display content method, updated all ui when a new element is placed in Inspector
        :param content: StorageObject
        :return: void
        """
        # print(content.parent_shelf_id)
        shelf_type = StoreFloor.get_shelf_by_id(content.parent_shelf_id)    # no error
        # print(shelf_type)
        if shelf_type:
            self.draw_type_cb(shelf_type)

        if content.container_type():
            self.container_instance = content.container_instance()
            type_index = self.find_cb_index(self.type_cb, content.container_type())
            self.type_cb.setCurrentIndex(type_index)

            if self.subtype_cb.currentIndex() != -1:
                # itemData in subtype_cb is instance of container (with dimensions)
                # storage_object.container_type() is the type of container
                subtype_index = self.find_cb_index(self.subtype_cb, content.container_instance())
                if subtype_index != -1:
                    self.subtype_cb.setCurrentIndex(subtype_index)



    def update_information_old(self, element: StorageObject):
        """
        OLD
        Updates informations to display good information on the selection part of the widget to select container
        according to shelf
        could be simplified
        :param element:
        :return:
        """
        if hasattr(element, 'parent_shelf_id'):
            shelf_target = StoreFloor.get_shelf_by_id(element.parent_shelf_id)
            self.draw_type_cb(shelf_target)
            self.draw_subtype_cb()
            # print('test3')
        else:
            self.display_blank()



