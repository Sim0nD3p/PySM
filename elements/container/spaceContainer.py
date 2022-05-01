import numpy as np

from elements.container.container import *
from elements.elementsTypes import *


class SpaceContainer(Container):
    display_type = 'Espace assigné'
    type = SPACE_CONTAINER

    def __init__(self, name: str, length: float, width: float, height: float):
        super().__init__(
            name=name,
            length=length,
            width=width,
            height=height,
            container_type=SPACE_CONTAINER,
            weight_capacity=10,
            net_weight=0
        )

    @classmethod
    def init_from_xml(cls, xml_data):
        properties = xml_data.attrib
        geo = properties['geo'].removeprefix('[').removesuffix(']')
        geo = np.fromstring(geo, dtype=float, sep=' ')
        geometry = geo.reshape(3, 2)

        sc = cls(
            name=properties['name'],
            length=geometry[0, 0],
            width=geometry[0, 1],
            height=geometry[2, 1],
        )
        sc.set_geometry(geometry)

        content = properties['content'].removeprefix('[').removesuffix(']')
        content = content.split("' '")
        if content[0].removeprefix("'").isdigit():
            name = content[1].removesuffix("'")
            sc.set_content(int(content[0].removeprefix("'")), name)


        # sc.set_content(int(content[0]), str(content[1]))
        return sc

