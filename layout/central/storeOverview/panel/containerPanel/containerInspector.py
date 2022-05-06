from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.panel.containerPanel.childrens.selectContainer import *
from elements.shelf.shelf import Shelf
from elements.ElementLogic.StorageObject import *
from elements.store.dataClasses import *
import copy


class ContainerInspector(QTabWidget):

    container_list_update_signal = pyqtSignal(name='update_container_list')
    shelf_draw_signal = pyqtSignal(name='shelf_redraw')

    def __init__(self):
        super().__init__()
        self.storage_group = None

        self.container_selector = SelectContainer()
        self.container_selector.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.addTab(self.container_selector, 'Sélection')

        self.container_selector.part_selector.part_selection_signal.connect(self.handle_part_selection)
        self.container_selector.container_selector.container_change.connect(self.handle_container_change)
        self.container_selector.container_options.container_number_changed.connect(self.handle_container_number_change)
        self.container_selector.origin_selector.origin_change_signal.connect(self.handle_origin_change)
        self.container_selector.container_options.placement_changed.connect(self.handle_placement_change)




    def handle_part_selection(self, part_code: str):
        """
        Runs on user input change in partSelector
        :param part:
        :return: void
        """
        self.container_selector.container_options.part_code = part_code
        if self.storage_group:
            self.storage_group.part_code = part_code

    def handle_container_change(self, container: Container):
        self.container_selector.container_options.container_type = container

        if self.storage_group:
            pass
            # self.storage_group.change_container_type(container)

    def handle_placement_change(self, index: int):
        """

        :param index: configuration index in the placement array returned by ContainerPlacement
        :return:
        """
        container_instance = self.container_selector.container_selector.get_container_instance()
        placement_options = ContainerPlacement.get_placement(container_instance=container_instance,
                                                             number=self.storage_group.container_number()
                                                             )
        print('handling placement change, index is ', index)
        if index < len(placement_options):
            self.storage_group.placement = placement_options[index]

        self.storage_group.move_containers()
        self.shelf_draw_signal.emit()
        print('containers shouldve moved')





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
            print('change in container number')


    def handle_submit(self):
        if self.storage_group:
            print('storage_group geometry', self.storage_group.geometry)

            # GET DATA FROM SUB WIDGETS
            part = self.container_selector.part_selector.get_part()
            container_instance = self.container_selector.container_selector.get_container_instance()
            container_options = self.container_selector.container_options.get_options_data()
            group_origin = self.container_selector.origin_selector.get_origin()

            # Setting storage_object origin
            self.storage_group.set_x_position(group_origin[0])
            self.storage_group.set_y_position(group_origin[1])

            # updating containers
            self.storage_group.update_containers(part, container_instance, container_options)
            self.storage_group.move_containers()

            # Put the storage_object back in shelf content list
            if self.storage_group.parent_shelf_id:
                shelf = StoreFloor.get_shelf_by_id(self.storage_group.parent_shelf_id)
                # print('hello')
                if self.storage_group not in shelf.storage_objects:
                    shelf.storage_objects.append(self.storage_group)

            self.container_list_update_signal.emit()

            self.storage_group = None
            self.display_blank()
            self.shelf_draw_signal.emit()

    def handle_origin_change(self, x, y):
        if issubclass(type(self.storage_group), StorageObject):
            self.storage_group.set_x_position(x)
            self.storage_group.set_y_position(y)
            self.storage_group.move_containers()

            self.shelf_draw_signal.emit()


    def display_blank(self):
        # print('containerInspector calls to display blank')
        self.container_selector.part_selector.display_blank()
        self.container_selector.container_selector.display_blank()
        self.container_selector.container_options.display_blank()
        self.container_selector.origin_selector.display_blank()


    def update_information(self, element: StorageObject):
        """
        Takes storage object and handle the container inspector
        :param element:
        :return:
        """
        if element:
            self.storage_group = element
            self.container_selector.update_child_widgets(self.storage_group)



