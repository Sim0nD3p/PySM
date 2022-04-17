from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.panel.containerPanel.childrens.selectContainer import *
from elements.shelf.shelf import Shelf
from elements.ElementLogic.StorageObject import *
import copy


class ContainerInspector(QTabWidget):

    container_list_update_signal = pyqtSignal(name='update_container_list')

    def __init__(self):
        super().__init__()
        self.storage_group = None

        self.container_selector = SelectContainer()
        self.addTab(self.container_selector, 'Sélection')

        self.container_selector.part_selector.part_selection_signal.connect(self.handle_part_selection)
        self.container_selector.container_selector.container_change.connect(self.handle_container_change)
        self.container_selector.container_options.container_number_changed.connect(self.handle_container_number_change)




    def handle_part_selection(self, part: Part):
        """
        Runs when user selects a part in the inspector part selector, sets the part code in StorageGroup (storageObject)
        :param part:
        :return: void
        """
        # print('handling part selection in containerInspector')
        # print(part)
        if self.storage_group:
            self.storage_group.set_part_code(part.code)

    def handle_container_change(self, container_type, length, width, height):
        """
        Handles change in container
        :param container_type:
        :param length:
        :param width:
        :param height:
        :return:
        """
        if container_type == Bin:
            container = Bin(name='test', length=length, width=width, height=height)
        elif container_type == SpaceContainer:
            container = SpaceContainer(name='test', length=length, width=width, height=height)
        else:
            # print('error @containerInspector, handle_container_change')
            pass

        if type(self.storage_group) == StorageObject:
            self.storage_group.change_containers(container)

        # change container method directly in storageObject
        # update positions of container (module)

    def get_container_old(self):
        """
        Gets the selected container and its dimensions
        :return:
        """
        type_cb_index = self.container_selector.container_selector.type_cb.currentIndex()
        type_cb_data = self.container_selector.container_selector.type_cb.itemData(type_cb_index)
        # print('type_cb_data')
        # print(type_cb_data)
        subtype_cb_index = self.container_selector.container_selector.subtype_cb.currentIndex()
        subtype_cb_data = self.container_selector.container_selector.subtype_cb.itemData(subtype_cb_index)
        # print('subtype_cb_data')
        # print(subtype_cb_data)

    def handle_container_number_change(self, value):
        if type(self.storage_group) == StorageObject:
            self.storage_group.set_nb_containers(value)

    def handle_submit(self):
        # print('StorageObject')
        if issubclass(type(self.storage_group), StorageObject):         # if the current object is StorageObject
            shelf = StoreFloor.get_shelf_by_id(self.storage_group.parent_shelf_id)  # we get the shelf by its id
            if self.storage_group not in shelf.storage_objects:
                shelf.add_storage(self.storage_group)
                self.container_list_update_signal.emit()
                self.update_information(None)




    # method to create StorageObject




    def update_information(self, element):
        """
        Dispatch update calls for different widget element
        could be way better
        :param element:
        :return:
        """
        print('ContainerInspector: receiving info on update method')
        if issubclass(type(element), StorageObject):
            self.storage_group = element
            self.container_selector.update_informations(element)
        elif not element:
            print('element absent')
            self.storage_group = None
            self.container_selector.update_informations(None)




