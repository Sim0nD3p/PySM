from elements.shelf.shelf import Shelf
from elements.elementsTypes import *
from elements.container.bin import *
from elements.container.spaceContainer import *
import numpy as np


class FlatShelf(Shelf):
    compatible_containers = [Bin, SpaceContainer]
    def __init__(self, name, id, length, width, height):
        super().__init__(name=name, id=id, type=FLAT_SHELF,
                         shelf_length=length, shelf_width=width,
                         shelf_height=height, x_position=0, y_position=0
                         )


    @classmethod
    def init_from_xml(cls, xml_data):
        """
        Initiate FlatShelf from xml data
        * could be better, streamlined
        :param xml_data:
        :return:
        """
        properties = xml_data.attrib
        if 'geometry' in properties:
            geo = properties['geometry'].removeprefix('[').removesuffix(']')
            geo = np.fromstring(geo, dtype=float, sep=' ')
            geometry = geo.reshape(3, 2)
            sh = cls(
                name=properties['name'],
                id=int(properties['id']),
                length=geometry[0, 0],
                width=geometry[0, 1],
                height=geometry[2, 1],
            )
            sh.set_x_position(geometry[1, 0])
            sh.set_y_position(geometry[1, 1])
            sh.set_height(geometry[2, 1])
            sh.set_angle(geometry[2, 0])
            return sh

