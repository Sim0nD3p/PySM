import numpy as np
from PyQt6.QtGui import *
from PyQt6.QtCore import *


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

    def __eq__(self, other):
        comparison = []
        if isinstance(other, Racking):
            for prop in vars(self):
                try:
                    if self.__getattribute__(prop) == other.__getattribute__(prop):
                        comparison.append(True)
                    else:
                        comparison.append(False)
                except ValueError:
                    if type(self.__getattribute__(prop)) == np.ndarray:
                        if np.array_equal(self.__getattribute__(prop), other.__getattribute__(prop)):
                            comparison.append(True)
                        else:
                            comparison.append(False)
                    else:
                        comparison.append(False)
                        print('ERROR - cannot compare elements in racking.__eq__()')

        return all(comparison)



    def height_map(self):
        """
        Returns a dict of the height map in range(base_height, max_height)
        {shelf_name: range(baseHeight, base_height + shelf_height)
        :return:
        """
        hmap = {}
        for shelf in self.shelves:
            r = range(int(shelf.base_height), int(shelf.base_height) + int(shelf.height()))
            hmap[shelf.name] = r
        return hmap


    def check_height_conflict(self, height_range: range):
        shelf_dict = {}
        for shelf in self.shelves:
            shelf_dict[shelf.name] = range(int(shelf.base_height), int(shelf.base_height) + int(shelf.height()))


    def set_base_height(self, base_height):
        pass

    def face_painter_path(self):
        path = QPainterPath()

        path.moveTo(QPointF(0, 0))
        path.lineTo(QPointF(0, self.height()))

        path.moveTo(QPointF(self.length(), 0))
        path.lineTo(QPointF(self.length(), self.height()))

        return path




    def add_shelf(self, shelf):
        """
        TODO Need to be better
        * check baseHeight
        :param shelf:
        :return:
        """
        print('add shelf')
        height_map = []
        ts = set(range(int(shelf.base_height), int(shelf.base_height) + int(shelf.height())))
        print(self.height_map())
        hmap = self.height_map()
        print(hmap)
        for key in hmap.keys():
            s = set(hmap[key])
            if set.intersection(ts, s):
                print('yesyt')



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


