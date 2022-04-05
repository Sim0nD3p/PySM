from layout.settings.settings import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from shapely import *
from shapely.geometry import *
from elements.container.container import *
import numpy as np
from elements.ElementLogic.dataClasses import *
from elements.ElementLogic.dataClasses import *

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

    """
    def __init__(self, name, shelf_length, shelf_width, shelf_height, x_position, y_position, type):
        super().__init__(length=shelf_length, width=shelf_width,
                         x_position=x_position, y_position=y_position,
                         angle=angle, height=shelf_height
                         )
        self.name = name
        self.type = type

        self.containers = []



    @classmethod
    def get_geometry_from_xml(cls, xml_data):

        print('initiating shelf from xml')
        properties = xml_data.attrib
        if 'geometry' in properties:
            geo = properties['geometry'].removeprefix('[').removesuffix(']')
            geo = np.fromstring(geo, dtype=float, sep=' ')
            geometry = geo.reshape(3, 2)







    def add_container(self, container: Container, position: Position):
        """
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






