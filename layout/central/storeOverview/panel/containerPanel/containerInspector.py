from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.panel.containerPanel.childrens.selectContainer import *
from elements.shelf.shelf import Shelf
from elements.ElementLogic.StorageObject import *
from elements.ElementLogic.dataClasses import *
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
        self.container_selector.container_selector.dimensions_change.connect(self.handle_dimensions_change)




    def handle_part_selection(self, part_code: str):
        """
        Runs on user input change in partSelector
        :param part:
        :return: void
        """
        self.container_selector.container_options.part_code = part_code
        if issubclass(type(self.storage_group), StorageObject):
            print('updating containers names')
            self.storage_group.set_part_code(part_code)


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
        placement_options = ContainerPlacement.get_placement_options(container_instance=container_instance,
                                                                     number=self.storage_group.container_number()
                                                                     )
        # print('handling placement change, index is ', index)
        if index < len(placement_options):
            self.storage_group.placement = placement_options[index]

        self.storage_group.move_containers()
        self.shelf_draw_signal.emit()
        # print('containers shouldve moved')

    def handle_container_number_change(self, value):
        if issubclass(type(self.storage_group), StorageObject):
            part_code = self.container_selector.part_selector.get_part()
            container_instance = self.container_selector.container_selector.get_container_instance()
            if container_instance and part_code:
                container_options = self.container_selector.container_options.get_options_data()
                self.container_selector.container_options.draw_placement_cb()
                self.storage_group.placement = None
                self.storage_group.update_containers(part=part_code,
                                                     container_instance=container_instance,
                                                     container_options=container_options
                                                     )

            # print('shouldve updated containers')
            self.shelf_draw_signal.emit()

    def handle_origin_change(self, x, y):
        if issubclass(type(self.storage_group), StorageObject):
            self.storage_group.set_x_position(x)
            self.storage_group.set_y_position(y)
            self.storage_group.move_containers()

            self.shelf_draw_signal.emit()

    def handle_dimensions_change(self, dimensions: Dimensions):
        """
        Handle dimensions change from containerSelector->dimensionsSelector
        :param dimensions:
        :return:
        """
        if issubclass(type(self.storage_group), StorageObject):
            if self.storage_group.container_instance():
                instance = self.storage_group.container_instance()
                if instance:
                    part = self.container_selector.part_selector.get_part()     # getting part name
                    storage_options = self.container_selector.container_options.get_options_data()  # getting options
                    instance.set_length(dimensions.length)      # setting dimensions
                    instance.set_width(dimensions.width)
                    instance.set_height(dimensions.height)
                    if self.storage_group.placement:
                        placement_index = ContainerPlacement.get_placement_index(self.storage_group.placement)
                        new_placements = ContainerPlacement.get_placement_options(container_instance=instance,
                                                                                  number=storage_options.nb_cont)

                        if new_placements and type(placement_index) == int:
                            new_placement = new_placements[placement_index-1]
                            self.storage_group.placement = new_placement

                    self.storage_group.update_containers(part=part, container_instance=instance,
                                                         container_options=storage_options)

                    self.storage_group.move_containers()
                    self.shelf_draw_signal.emit()





    def handle_submit(self):
        if self.storage_group:

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

    def handle_delete(self):
        """
        Handles deletion of the current storage_object form the shelf content
        :return:
        """
        print('handling delete')
        if issubclass(type(self.storage_group), StorageObject) and self.storage_group.parent_shelf_id:
            shelf = StoreFloor.get_shelf_by_id(self.storage_group.parent_shelf_id)
            if shelf:
                shelf.storage_objects.remove(self.storage_group)
                self.display_blank()
                self.storage_group = None
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
            # TODO change how storage_object is added to shelf.contentObjects
            # TODO handle container size change for custom size containers
            if self.storage_group.parent_shelf_id:
                shelf = StoreFloor.get_shelf_by_id(self.storage_group.parent_shelf_id)
                # print('hello')
                if self.storage_group not in shelf.storage_objects:
                    shelf.storage_objects.append(self.storage_group)

            self.container_selector.update_child_widgets(self.storage_group)



