import numpy as np
from elements.elementsTypes import *
from elements.store.storeObject import StoreObject
from math import cos, sin, radians as rad
"""
Racking need dimensions, position, name

"""
class Racking(StoreObject):
    def __init__(self, name, id, x_position, y_position, width, length, angle, height):
        super().__init__(
            name=name,
            id=id,
            x_position=x_position,
            y_position=y_position,
            width=width,
            length=length,
            angle=angle,
            height=height,
            element_type=RACKING
        )
        self.shelves = []
        """
        racking have shelves:
        shelves should be represented by matrices in racking
        """
    def add_shelf(self, shelf):
        """
        TODO Need to be better
        :param shelf:
        :return:
        """
        self.shelves.append(shelf)

    def set_length(self, length):
        """
        override geometry method to also change the length of shelves
        :param length:
        :return:
        """
        for shelf in self.shelves:
            if shelf.length() == self.length():
                shelf.set_length(length)

        super(Racking, self).set_length(length)     # calls the parent method to change length

    def set_width(self, width):
        for shelf in self.shelves:
            if shelf.width() == self.width():
                shelf.set_width(width)

        super(Racking, self).set_width(width)   # calls the parent method to change width



    @classmethod
    def init_from_xml(cls, xml_data):
        """
        Initiate object from xml data with attributes in shape of dict, geometry_matrix is in string
        :param xml_data:
        :return:
        """
        properties = xml_data.attrib
        geo = properties['geometry'].removeprefix('[').removesuffix(']')
        geo = np.fromstring(geo, dtype=float, sep=' ')
        geometry = geo.reshape(3, 2)
        ra = cls(
            name=properties['name'],
            id=properties['id'],
            length=geometry[0, 0],
            width=geometry[0, 1],
            x_position=geometry[1, 0],
            y_position=geometry[1, 1],
            angle=geometry[2, 0],
            height=geometry[2, 1],
        )
        return ra


