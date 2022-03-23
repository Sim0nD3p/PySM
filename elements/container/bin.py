from elements.container.container import *
import numpy as np
from elements.elementsTypes import *
from layout.settings.settings import *

class Bin(Container):
    weight_capacity = Settings.bin_weight_capacity
    def __init__(self, name: str, length: float, width: float, height=float, ):
        super().__init__(
            name=name,
            container_type=BIN,
            length=length,
            width=width,
            height=height,
        )



    @classmethod
    def set_weight_capacity(cls, weight_capacity: float):
        """
        Sets the weight capacity for the whole bin class
        **what happens when the limit changes to lower than the current number of parts
        :param weight_capacity:
        :return:
        """
        cls.weight_capacity = weight_capacity


