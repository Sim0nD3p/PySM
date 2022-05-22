import math

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

    Name of placement:
        cont + [nb of container] + _ + [index of the configuration]
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
        return [
            [cont1],    # cont1_1
            [cont2]     # cont1_2
        ]

    @classmethod
    def cont2_options(cls, container):
        # TODO check container place on shelf how width and length are handled switched?
        cont1_1 = Geo2dMatrix(length=container.length(), width=container.width(),
                              x_position=0, y_position=0)
        cont1_2 = Geo2dMatrix(length=container.length(), width=container.width(),
                              x_position=0, y_position=cont1_1.width())

        cont2_1 = Geo2dMatrix(length=container.width(), width=container.length(),
                              x_position=0, y_position=0)
        cont2_2 = Geo2dMatrix(length=container.width(), width=container.length(),
                              x_position=cont2_1.length(), y_position=0)

        cont3_1 = Geo2dMatrix(length=container.width(), width=container.length(),
                              x_position=0, y_position=0)
        cont3_2 = Geo2dMatrix(length=container.width(), width=container.length(),
                              x_position=0, y_position=cont3_1.width())

        return [
            [cont1_1, cont1_2],     # cont2_1
            [cont2_1, cont2_2],     # cont2_2
            [cont3_1, cont3_2],     # cont2_3
        ]

    @classmethod
    def cont3_options(cls, container):
        pass

    @classmethod
    def get_placement_options(cls, container_instance: Container, number: int):
        """
        Get placement, list of Geo2dMatrix for the relative position of the containers
        :param container_instance:
        :param number:
        :return:
        """
        if number == 1:
            return cls.cont1_options(container_instance)
        elif number == 2:
            return cls.cont2_options(container_instance)
        else:

            print('error in get_placement (containerPlacement)')
            return cls.cont1_options(container_instance)

    @classmethod
    def get_placement_index(cls, placement):
        """
        Splits the placement name to get the index at the end
        :param placement_name:
        :return: int (index)
        """
        placement_name = cls.get_placement_name(placement)
        if placement_name:
            try:
                i = int(placement_name.split('_')[1])
                return i
            except ValueError:
                return placement_name
        else:
            return 'Error'


    @classmethod
    def get_placement_name(cls, placement):
        """
        Gets the name of the placement to store in xml file
        Creates placement as we would do for a container from placement infos
        Compare placement data to list from the creation of placements to get index and name
        :param placement:
        :return:
        """
        g2m_sample = placement[0]

        length = max(g2m_sample.length(), g2m_sample.width())
        width = min(g2m_sample.length(), g2m_sample.width())
        cont = Container('', '', length=length, width=width, height=0, net_weight=0, weight_capacity=0)

        options = []
        if len(placement) == 1:
            options = cls.cont1_options(cont)

        elif len(placement) == 2:
            options = cls.cont2_options(cont)

        elif len(placement) == 3:
            # options = cls.cont3_options(cont)
            # TODO ADD CONT3
            pass

        place_calc = []
        for place in placement:
            place_calc.append(np.array2string(place.geometry.flatten()))

        name = None
        for i in range(0, len(options)):
            current_option = []
            for opt_cont in options[i]:
                current_option.append(np.array2string(opt_cont.geometry.flatten()))
            if current_option == place_calc:
                name = 'cont' + str(len(placement)) + '_' + str(i + 1)

        return name

