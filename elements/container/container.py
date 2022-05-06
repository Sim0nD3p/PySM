import numpy as np
from elements.ElementLogic.dataClasses import *
from elements.elementsTypes import *
from elements.part.Part import Part

x_position = 0
y_position = 0
angle = 0


class Container(Geometry):
    """
    What should container do exactly?
    For container:
        - length: dimensions in length axis of shelf
        - width: dimensions in width axis of shelf
        - angle always 0 ->MAYBE NOT
        all containers should have geometry
    """
    weight_capacity = 1000  # should be changed
    display_type = 'container'
    type = CONTAINER

    def __init__(self, name: str, container_type: str, length: float, width: float, height: float,
                 weight_capacity: float, net_weight: float):
        """
        Init for parent of container

        Things to be setup:
            - contennt
            - stored_part
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
        self.stored_part = None     # DEPRECIATED, use content instead
        self.content = np.array([0, None])  # number of parts, part str
        self.type = container_type
        self.weight_capacity = weight_capacity  # weight capacity of the container
        self.net_weight = net_weight    # weight when empty

    def get_content(self):
        """
        Gets the content np.array([quantity, whats in the container])
        :return:
        """
        return self.content

    def set_content(self, number: int, content: str):
        """
        Sets the content of the container
        :param number: number of part in the container
        :param content: string reference to the content (parts code)
        :return: void
        """
        self.content = np.array([int(number), content])


    def set_position(self, x_position, y_position):
        pass

    def place_on_shelf(self, placement, so_origin):
        if placement.length() > placement.width():
            self.set_length(placement.length())
            self.set_width(placement.width())
            self.set_x_position(placement.x_position() + so_origin[0])
            self.set_y_position(placement.y_position() + so_origin[1])
            self.set_angle(0)
        elif placement.length() <= placement.width():
            self.set_length(placement.width())
            self.set_width(placement.length())
            self.set_x_position(placement.x_position() - placement.length() + so_origin[0])
            self.set_y_position(placement.y_position() + so_origin[1])










