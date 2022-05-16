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
            name='', length=0, width=0,
            x_position=0, y_position=0,
            angle=0, height=0
        )
        # we'll need to setup geometry later when posiotionning in shelf
        self.part_code = None
        self.parent_shelf_id = parent_shelf_id
        self.containers = [Bin('sample_bin', length=0, width=0, height=0)]    # at least 1 container

        # self.number_part = 0    # total number of parts in group DEPRECIATED
        self.placement = None

    def set_part_code(self, part_code: str):
        """
        Sets the part code of the group for which part is stored
        :param part_code:
        :return: void
        """
        self.part_code = part_code
        self.name = part_code       # inherited from geometry
        for i in range(0, len(self.containers)):
            if issubclass(type(self.containers[i]), Container):
                container_name = str(self.containers[i].type) + '_' + part_code + '_' + str(i)
                self.containers[i].name = container_name
        # update drawing of name label?

    def container_number(self):
        """
        Returns the number of containers in the group
        :return: int
        """
        return len(self.containers)

    def storage_capacity(self):
        capacity = 0
        for container in self.containers:
            if issubclass(type(container), Container):
                if issubclass(type(container), Container):
                    capacity += int(container.get_content()[0])
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
        """
        Called on handle submit
        placement is array of Geo2dMatrix containing (length, width in axis directions and positions)
        :param part:
        :param container_instance:
        :param container_options:
        :return:
        """
        containers = []
        print('updating containers updateContainers', container_instance.geometry)
        if container_options.nb_cont != 0:
            nb_part_cont = math.ceil(container_options.nb_part / container_options.nb_cont)

            if not self.placement:
                # print('drawing default placement')

                placement = ContainerPlacement.get_placement_options(container_instance=container_instance,
                                                                     number=container_options.nb_cont)
                if placement:
                    self.placement = placement[0]

            if self.placement:
                print('resetting placement', container_instance.geometry)


                for i in range(0, container_options.nb_cont):
                    cont_i = ContainerCatalog.create_containers(container_instance, 1)[0]   # creating new containers
                    cont_i.name = str(cont_i.type) + '_' + part + '_' + str(i)
                    cont_i.set_content(nb_part_cont, part)
                    containers.append(cont_i)

                self.containers = containers
                self.move_containers()



    def move_containers(self):
        """
        Calculates the position of the containers on shelf according to the placement and the origin of storage_object
        :return: void
        """
        if self.container_type() and self.placement and len(self.containers) == len(self.placement):
            for i in range(0, len(self.placement)):
                self.containers[i].place_on_shelf(placement=self.placement[i],
                                                  so_origin=[self.x_position(), self.y_position()])




    def set_nb_containers_old(self, nb_containers: int):
        """
        There is no set_container_number because changing the number of container require a change in placement
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




    def is_admissible_old(self):
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

            if len(containers) >= 1:
                instance.containers = containers

                placement = None
                if 'placement' in properties and issubclass(type(instance.container_instance()), Container) and \
                        len(properties['placement']) > 1:
                    index = properties['placement'].split('_')[len(properties['placement'].split('_')) - 1]
                    # print('index', index)
                    placement = ContainerPlacement.get_placement_options(container_instance=instance.container_instance(),
                                                                         number=instance.container_number())
                    if placement:
                        instance.placement = placement[int(index) - 1]
                        instance.move_containers()



            return instance










