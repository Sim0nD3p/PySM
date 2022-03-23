import numpy as np

x_position = None
y_position = None
angle = None


class Container:
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
        self.name = name
        self.type = container_type
        self.geometry = np.array([
            [length, width],
            [x_position, y_position],
            [angle, height]
        ])
        self.net_weight = 0     # TODO handle net-weight

        self.content = np.array([])     # should it be np.array?

    def weight(self):
        """
        Return total weight of the container
        :return:
        """
        total_weight = self.net_weight
        for element in self.content:
            if hasattr(element, 'weight'):
                total_weight += element.weight
        return total_weight




        # CAPACITY ?







