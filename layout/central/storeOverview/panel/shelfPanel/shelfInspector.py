from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.components.contextInterface.shelfProperties import *
from elements.racking.racking import *
from layout.components.contextInterface.shelfContent import *


class ShelfInspector(QTabWidget):
    shelf_list_update_signal = pyqtSignal(name='shelf_list_update')

    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.parent_racking = None
        self.element = None

        self.shelf_properties = ShelfProperties()
        self.addTab(self.shelf_properties, 'General')

        self.shelf_content = ShelfContent()
        self.addTab(self.shelf_content, 'Contenu')

    def handle_submit(self):
        if not self.element:
            self.create_shelf()
        elif issubclass(type(self.element), Shelf):
            print(vars(self.element))
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
        print('type')
        print(target_type)
        if target_type == FLAT_SHELF:
            print('shelf created and sent to racking')
            shelf = FlatShelf(
                name=self.shelf_properties.name_le.text(),
                length=self.shelf_properties.length_sb.value(),
                width=self.shelf_properties.width_sb.value(),
                height=self.shelf_properties.height_sb.value()
            )
            print('self')
            print(shelf)
            print(self.parent_racking)
            self.parent_racking.add_shelf(shelf)
            self.shelf_list_update_signal.emit()


    def update_child_information(self, element):
        """
        Calls update methods on all children to display shelf information
        :param element:
        :return:
        """
        self.shelf_properties.enable_all()
        print('update child infos shelf')
        if element is None:
            print('element None')
            self.shelf_properties.display_blank()
            self.shelf_content.display_blank()
            self.shelf_properties.element = None
            self.shelf_properties.disable_all()
        elif type(element) is ElementConstructorData:
            print('ElementConstructorData')
            self.element = None
            self.shelf_properties.element = element
            self.shelf_properties.update_information(element)
        elif issubclass(type(element), Shelf):
            print('type shelf')
            self.element = element
            self.shelf_properties.element = element
            self.shelf_properties.update_information(element)

