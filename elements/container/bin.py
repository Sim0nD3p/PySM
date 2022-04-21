from elements.container.container import *
import numpy as np
from elements.elementsTypes import *
from layout.settings.settings import *


class Bin(Container):
    weight_capacity = Settings.bin_weight_capacity
    display_type = 'Bac'
    type = BIN
    net_weight = 0.1     # net weight for all bin (approximation)

    def __init__(self, name: str, length: float, width: float, height: float):
        super().__init__(
            name=name,
            container_type=BIN,
            length=length,
            width=width,
            height=height,
            weight_capacity=self.weight_capacity,     # setting weight capacity
            net_weight=self.net_weight
        )



