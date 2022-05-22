from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.components.contextInterface.shelfProperties import *
from elements.racking.racking import *
from layout.components.contextInterface.shelfContent import *
from elements.shelf.shelf import *
from elements.store.dataClasses import *
from elements.shelf.flatShelf import *
from elements.ElementLogic.StorageObject import *
from backend.storeFloor import *


class ShelfInspector(QTabWidget):
    shelf_list_update_signal = pyqtSignal(name='shelf_list_update')
    # start_container_creation = pyqtSignal(Shelf, name='start_creation')
    container_select_signal = pyqtSignal(StorageObject, name='new_container')

    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.parent_racking = None
        self.element = None

        self.shelf_properties = ShelfProperties()
        self.addTab(self.shelf_properties, 'General')

        self.shelf_content = ShelfContent()
        self.addTab(self.shelf_content, 'Contenu')

        self.shelf_content.add_button.clicked.connect(self.start_container_path)
        self.shelf_content.list.itemClicked.connect(self.handle_shelf_content_click)

    # TODO: hide shelfViewer when shelf unselect


    def handle_delete(self):
        print('handling delete from shelfInspector')

    def handle_submit(self):
        if not self.element:
            self.create_shelf()
        elif issubclass(type(self.element), Shelf):
            # print(vars(self.element))
            self.shelf_properties.modify_shelf_properties()
        self.element = None

    def set_parent_racking(self, racking: Racking):
        """
        Sets parent racking to given racking
        :param racking:
        :return:
        """
        self.parent_racking = racking

    def create_shelf(self):
        """
        Creates the shelf object and adds it to racking object
        :return:
        """
        target_type = self.shelf_properties.type_cb.itemData(self.shelf_properties.type_cb.currentIndex())
        # print('type')
        # print(target_type)
        if target_type == FLAT_SHELF:
            # print('shelf created and sent to racking')
            shelf = FlatShelf(
                name=self.shelf_properties.name_le.text(),
                id=StoreFloor.generate_id(),
                length=self.shelf_properties.length_sb.value(),
                width=self.shelf_properties.width_sb.value(),
                height=self.shelf_properties.height_sb.value()
            )
            # print('self')
            # print(shelf)
            # print(self.parent_racking)
            shelf.set_parent_racking(self.parent_racking)
            self.parent_racking.add_shelf(shelf)
            self.shelf_list_update_signal.emit()

    def start_container_path(self):
        """
        Initiate the creation of a StorageObject which group containers for a given part on a shelf
        :return:
        """
        storage_object = StorageObject(parent_shelf_id=self.element.id)
        # print('shelfInspector: Emitting signal for new StorageObject ', self.element.id)
        self.container_select_signal.emit(storage_object)

    def handle_shelf_content_click(self, item: QListWidgetItem):
        """
        Handles element click on the shelf content container list
        :param item: QListWidgetItemstore
        :return: void
        """
        data = item.data(1)
        if issubclass(type(item.data(1)), StorageObject):
            self.container_select_signal.emit(item.data(1))



    def update_content_list(self):
        """
        Updates the child list of content with data from the current element in inspector
        :return: void
        """
        # print('updating shelf content list')
        # print('type self.element', type(self.element))
        # print(help(self.shelf_content.list))
        print('fix bug')
        # self.shelf_content.list.clear()         # TODO FIX BUG SHOULD CLEAR LIST BUT THE COMMANDS BUG
        self.shelf_content.list.clear()
        if issubclass(type(self.element), Shelf):
            # print('bon')
            for element in self.element.storage_objects:
                item = QListWidgetItem(element.part_code)
                item.setData(1, element)
                self.shelf_content.list.addItem(item)




    def update_child_information(self, element):
        """
        Calls update methods on all children to display shelf information
        :param element:
        :return:
        """
        self.shelf_properties.enable_all()
        # print('update child infos shelf')
        if element is None:
            # print('element None')
            self.shelf_properties.display_blank()
            self.shelf_content.display_blank()
            self.shelf_properties.element = None
            self.shelf_properties.disable_all()
        elif type(element) is ElementConstructorData:
            # print('ElementConstructorData')
            self.element = None
            self.shelf_properties.element = element
            self.shelf_properties.update_information(element)
        elif issubclass(type(element), Shelf):
            # print('type shelf')
            self.element = element
            self.shelf_properties.element = element
            self.shelf_properties.update_information(element)
            self.shelf_content.update_information(element)  # kinda useless? (list updated from shelfInspector)
            self.update_content_list()


