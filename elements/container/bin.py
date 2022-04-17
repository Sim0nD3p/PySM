from elements.container.container import *
import numpy as np
from elements.elementsTypes import *
from layout.settings.settings import *


class Bin(Container):
    weight_capacity = Settings.bin_weight_capacity
    display_type = 'Bac'
    type = BIN

    def __init__(self, name: str, length: float, width: float, height: float):
        super().__init__(
            name=name,
            container_type=BIN,
            length=length,
            width=width,
            height=height,
            weight_capacity=33,     # setting weight capacity
            net_weight=323,        # from saved preset
        )



