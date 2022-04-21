import math

from elements.ElementLogic.dataClasses import *
from elements.container.container import *
import numpy as np
import copy
from backend.ContainerCatalog import *
from PyQt6.QtGui import *


class StorageObject(Geometry):
    """
    Properties of group of containers
    maybe not inherit geometry
    should inherit geometry, for position at least
    """
    def __init__(self, parent_shelf_id):
        super().__init__(
            length=0, width=0,
            x_position=0, y_position=0,
            angle=0, height=0
        )
        # we'll need to setup geometry later when posiotionning in shelf
        self.part_code = None
        self.parent_shelf_id = parent_shelf_id
        self.containers = [None]    # at least 1 container

        self.number_part = 0    # total number of parts in group
        self.disposition = None

    def set_part_code(self, part_code: str):
        """
        Sets the part code of the group for which part is stored
        :param part_code:
        :return: void
        """
        self.part_code = part_code

    def container_number(self):
        """
        Returns the number of containers in the group
        :return: int
        """
        return len(self.containers)

    def storage_capacity(self):
        capacity = 0
        print('storage capacity', self.containers)
        for container in self.containers:
            if issubclass(type(container), Container):
                print('getting container', container.name, container.get_content())
                if issubclass(type(container), Container):
                    capacity += int(container.get_content()[0])
                    print('capacity increase', container.get_content())
            print('storage capacity', capacity)
        return capacity

    def nb_part_cont_old(self):
        """
        Returns the number of parts per container
        :return: int
        """
        return self.storage_capacity() / self.container_number()

    def container_type(self):
        """
        Returns the type of container in group
        :return: type
        """
        return type(self.containers[0])

    def update_containers(self, number: int, container_type: type, container_options: dict, part_number: int):
        containers = ContainerCatalog.create_containers(class_type=container_type, number=number,
                                                        options=container_options
                                                        )
        # get disposition before assigning it in next loop
        nb_part_cont = math.ceil(part_number/number)
        print('nb_part_cont', nb_part_cont)

        for container in containers:
            container.set_content(nb_part_cont, self.part_code)
            print('updating container', container.name, container.get_content())

        self.containers = containers


    def set_nb_containers_old(self, nb_containers: int):
        """
        Sets the container quantity of the storage object
        :param nb_container:
        :return: void
        """
        self.nb_containers = nb_containers
        # TODO will need to run some updates to the group

    def change_container_type(self, target_container: Container):
        """
        Handles the change in container type, should be checked
        :param target_container:
        :return:
        """
        new_containers = []
        for container in self.containers:
            # is substitute function in container object?
            # init new_container with class method init_from_container?
            new_container = target_container
            new_containers.append(new_container)

        self.containers = new_containers


    def is_admissible(self):
        """
        Checks if the StorageObject is admissible to shelf
        :return:
        """
        if self.nb_containers != 0 and self.disposition is not None:
            return True
        else:
            return False





