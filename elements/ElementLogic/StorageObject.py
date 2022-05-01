import math

from elements.ElementLogic.dataClasses import *
from elements.container.container import *
import numpy as np
from elements.store.dataClasses import *
import copy
from backend.ContainerCatalog import *
from PyQt6.QtGui import *
from elements.ElementLogic.containerPlacement import ContainerPlacement


class StorageObject(Geometry):
    """
    Properties of group of containers
    maybe not inherit geometry
    should inherit geometry, for position at least
    TODO have method to check for overall width and length, shapely, vectors
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

        # self.number_part = 0    # total number of parts in group DEPRECIATED
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
        # print('storage capacity', self.containers)
        for container in self.containers:
            if issubclass(type(container), Container):
                # print('getting container', container.name, container.get_content())
                if issubclass(type(container), Container):
                    capacity += int(container.get_content()[0])
                    # print('capacity increase', container.get_content())
            # print('storage capacity', capacity)
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
        if self.containers[0]:
            return type(self.containers[0])
        else:
            return None

    def container_instance(self):
        """
        Returns an instance of the first container **USE TO READ ONLY
        :return: Container
        """
        return self.containers[0]

    def update_containers(self, part: str, container_instance: Container, container_options: ContainerOptions):
        # TODO create array of container with all properties
        containers = []
        nb_part_cont = math.ceil(container_options.nb_part / container_options.nb_cont)
        placement = ContainerPlacement.get_placement(container_instance=container_instance,
                                                     number=container_options.nb_cont)[0]  # TODO [0] should be option
        for i in range(0, container_options.nb_cont):
            cont_i = ContainerCatalog.create_containers(container_instance, 1)[0]
            cont_i.set_content(nb_part_cont, part)
            so_origin = [self.x_position(), self.y_position()]
            print(placement[i])
            print('so_origin', so_origin)
            cont_i.place_on_shelf(placement=placement[i], so_origin=so_origin)
            containers.append(cont_i)





        self.containers = containers





    def set_nb_containers_old(self, nb_containers: int):
        """
        Sets the container quantity of the storage object
        :param nb_container:
        :return: void
        """
        self.nb_containers = nb_containers
        # TODO will need to run some updates to the group

    def change_container_type(self, container_instance: Container):
        """
        Changes the container type to the given container, creates containers based on the type
        Number of containers is unchanged
        :param container_instance:
        :return:
        """
        new_containers = []
        for cont in self.containers:
            n_cont = ContainerCatalog.create_containers(container_instance=container_instance, number=1)[0]
            if issubclass(type(cont), Container):
                # transferring data from old container to new container
                n_cont.set_content(cont.get_content()[0], cont.get_content()[1])
                # TODO will be more data to add into transfer

            new_containers.append(n_cont)

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

    @classmethod
    def init_from_xml(cls, xml_data):
        """
        Initiates the storage_object and containers
        :param xml_data:
        :return:
        """
        properties = xml_data.attrib
        if 'parent_shelf_id' in properties:
            instance = cls(int(properties['parent_shelf_id']))
            instance.set_part_code(properties['part_code'])
            # TODO SET GEOMETRY
            geo = properties['geo'].removeprefix('[').removesuffix(']')
            geo = np.fromstring(geo, dtype=float, sep=' ')
            geometry = geo.reshape(3, 2)
            instance.set_geometry(geometry)

            # creating containers
            containers = []
            for xml_cont in xml_data:
                if xml_cont.tag == BIN:
                    container = Bin.init_from_xml(xml_cont)
                    containers.append(container)

                elif xml_cont.tag == SPACE_CONTAINER:
                    container = SpaceContainer.init_from_xml(xml_cont)
                    containers.append(container)
                else:
                    pass
            instance.containers = containers

            return instance










