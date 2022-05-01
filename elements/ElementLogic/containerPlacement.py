import numpy as np

from elements.container.container import Container


class Geo2dMatrix:
    def __init__(self, length, width, x_position, y_position):
        """

        :param length: position in the x axis (long side of ths shelf)
        :param width: position in the x axis (long side of ths shelf)
        :param x_position: position in the x axis
        :param y_position: position in the y axis
        """
        self.geometry = np.array([
            [length, width],
            [x_position, y_position]
        ])

    def length(self):
        return self.geometry[0][0]

    def width(self):
        return self.geometry[0][1]

    def x_position(self):
        return self.geometry[1][0]

    def y_position(self):
        return self.geometry[1][1]





class ContainerPlacement:
    """
    Standards:
    for container: length is the biggest side, width is the smallest side
    for Geo2dMatrix:
        - x_position: position in the x axis (long side of ths shelf)
        - y_position: position in the y axis (short side of the shelf)
        - length: position in the x axis
        - width: position on the y axis
    """
    def __init__(self):
        pass

    @classmethod
    def test(cls):
        print('this is test')

    @classmethod
    def cont1_options(cls, container):
        cont1 = Geo2dMatrix(length=container.length(), width=container.width(),
                            x_position=0, y_position=0
                            )
        cont2 = Geo2dMatrix(length=container.width(), width=container.length(),
                            x_position=0, y_position=0)
        return [[cont1, cont2]]

    @classmethod
    def cont2_options(cls, container):
        cont1_1 = Geo2dMatrix(length=container.length(), width=container.width(),
                              x_position=0, y_position=0)
        cont1_2 = Geo2dMatrix(length=container.length(), width=container.width(),
                              x_position=0, y_position=cont1_1.width())

        cont2_1 = Geo2dMatrix(length=container.width(), width=container.length(),
                              x_position=0, y_position=0)
        cont2_2 = Geo2dMatrix(length=container.width(), width=container.length(),
                              x_position=cont2_1.length(), y_position=0)

        return [
            [cont1_1, cont1_2],
            [cont2_1, cont2_2]
        ]

    @classmethod
    def get_placement(cls, container_instance: Container, number: int):
        if number == 1:
            return cls.cont1_options(container_instance)
        elif number == 2:
            return cls.cont2_options(container_instance)
        else:
            return None


    @classmethod
    def assign_placement(cls, placement, containers):
        if not placement:
            if len(containers) == 1:
                placement = cls.cont1_options(containers[0])[0]
            elif len(containers) == 2:
                placement = cls.cont2_options(containers[0])[0]

        print('placement length', len(placement), placement)
        if len(placement) == len(containers):
            for i in range(0, len(placement)):
                print(placement[i].geometry)
                containers[i].place_on_shelf(placement[i])

        return containers



