from layout.settings.settings import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from elements.container.container import *
import numpy as np
from elements.ElementLogic.dataClasses import *
from elements.ElementLogic.dataClasses import *
from elements.ElementLogic.StorageObject import *
"""
Multiple shelves style:
- flat
"""
content_height = 0
net_height = Settings.default_shelf_net_height


class Shelf(Geometry):
    """
    Parent class for shelf
    What should shelf do exactly

    about position: shelf have x and y positions (usually 0, 0), about where they are placed on racking\
    with origin in bottom left corner
    Dimension:
    - length is the dimensions in the length/width axis of the shelf
    - width is the dimensinos in the depth axis of the shelf

    """
    compatible_containers = []

    def __init__(self, name, id, shelf_length, shelf_width, shelf_height, x_position, y_position, type):
        super().__init__(name=name, length=shelf_length, width=shelf_width,
                         x_position=x_position, y_position=y_position,
                         angle=angle, height=shelf_height
                         )
        self.name = name
        self.type = type
        self.id = id
        self.parent_racking = None

        self.storage_objects = []   # storage object regrouping all containers

                                    # should be replaced by self.containers()


    def set_parent_racking(self, racking):
        """
        Sets the parent racking value of shelf, cannot put full racking object since shelf is in racking (loop)
        checks if shelf and racking are compatible in dimensions and put the racking name and id in property
        :param racking:
        :return:
        """



    @classmethod
    def get_geometry_from_xml(cls, xml_data):

        print('initiating shelf from xml')
        properties = xml_data.attrib
        if 'geometry' in properties:
            geo = properties['geometry'].removeprefix('[').removesuffix(']')
            geo = np.fromstring(geo, dtype=float, sep=' ')
            geometry = geo.reshape(3, 2)

    def containers(self):
        """
        gets the container list from all storage_group
        :return:
        """
        container_list = []
        for group in self.storage_objects:
            for container in group.containers:
                if container:
                    container_list.append(container)

        return container_list


    def find_storage_group(self, container: Container):
        """
        Find the storage_group parent to the given container
        :param container: Container
        :return:
        """
        pass

    def add_storage(self, storage_object: StorageObject):
        """
        Adds storage_object to self.storage_objects
        :param storage_object:
        :return:
        """
        self.storage_objects.append(storage_object)






    def add_container(self, container: Container, position: Position):
        """
        DEPRECIATED
        Check if container have position and add it to content
        # TODO check if all vertices are inside shelf
        :param container:
        :return:
        """
        print('adding container')
        print(container)
        container.set_x_position(position.x_position)
        container.set_y_position(position.y_position)
        container.set_angle(0)
        self.containers.append(container)

    def find_position(self, container: Container, position_type: str):
        """
        Ideas:
        - use transformation matrix in loop to find available spot
        :param container:
        :param position_type:
        :return:
        """
        pass







