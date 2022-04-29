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

    @classmethod
    def init_from_xml(cls, xml_data):
        properties = xml_data.attrib
        geo = properties['geo'].removeprefix('[').removesuffix(']')
        geo = np.fromstring(geo, dtype=float, sep=' ')
        geometry = geo.reshape(3, 2)

        bin = cls(
            name=properties['name'],
            length=geometry[0, 0],
            width=geometry[0, 1],
            height=geometry[2, 1],
        )
        content = properties['content'].removeprefix('[').removesuffix(']')
        content = content.split("' '")
        if content[0].removeprefix("'").isdigit():
            name = content[1].removesuffix("'")
            bin.set_content(int(content[0].removeprefix("'")), name)
        return bin



