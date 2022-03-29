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
        self.content = []
        """
        racking have shelves:
        shelves should be represented by matrices in racking
        """
    def add_content(self, element):
        pass

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
            length=geometry[1, 0],
            width=geometry[1, 1],
            x_position=geometry[0, 0],
            y_position=geometry[0, 1],
            angle=geometry[2, 0],
            height=geometry[2, 1],
        )
        return ra


