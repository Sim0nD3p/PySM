import numpy as np
from elements.ElementLogic.dataClasses import *

x_position = 0
y_position = 0
angle = 0


class Container(Geometry):
    """
    What should container do exactly?

    """
    def __init__(self, name: str, container_type: str, length: float, width: float, height: float, weight_capacity: float):
        """
        Init for parent of container
        :param name:
        :param container_type:
        :param length:
        :param width:
        :param height:
        """
        super().__init__(length=length, width=width,
                         x_position=x_position, y_position=y_position,
                         angle=angle, height=height
                         )
        self.name = name
        self.type = container_type
        self.net_weight = 0     # TODO handle net-weight





        # CAPACITY ?







