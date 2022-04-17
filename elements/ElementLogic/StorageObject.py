from elements.ElementLogic.dataClasses import *
from elements.container.container import *
import numpy as np
import copy
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
        self.containers = [None]
        self.nb_containers = 1
        self.part_cont = 0      # number of parts per container
        self.disposition = None

    def set_part_code(self, part_code: str):
        """
        Sets the part code of the group
        :param part_code:
        :return: void
        """
        self.part_code = part_code

    def container_type(self):
        """
        Returns the type of container in group
        :return: type
        """
        return type(self.containers[0])


    def set_nb_containers(self, nb_containers: int):
        """
        Sets the container quantity of the storage object
        :param nb_container:
        :return: void
        """
        self.nb_containers = nb_containers
        # TODO will need to run some updates to the group

    def change_containers(self, target_container: Container):
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




    def set_disposition(self, disposition):
        """
        Sets the disposition of the containers
        :param disposition:
        :return:
        """
        pass

    def update_width(self):
        """
        Not necessarly useful since object might have weird shape
        :return:
        """
        pass






    def set_geometry(self):
        pass

    def get_length(self):
        """
        length taken by container on shelf length (check orientation, angle)
        :return:
        """


    def is_admissible(self):
        """
        Checks if the StorageObject is admissible to shelf
        :return:
        """
        if self.nb_containers != 0 and self.disposition is not None:
            return True
        else:
            return False





