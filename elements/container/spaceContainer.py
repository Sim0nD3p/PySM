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
