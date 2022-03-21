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
