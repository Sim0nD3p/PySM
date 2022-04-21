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
        self.stored_part = None
        self.content = np.array([0, None])
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



    def get_stored_part(self):
        """
        Returns the stored part
        :return:
        """
        if issubclass(type(self.stored_part), Part):
            return self.stored_part
        else:
            return None


    def set_position(self, x_position, y_position):
        """
        Method to set the position of the container, sets the geometry
        :param x_position:
        :param y_position:
        :return:
        """









