import numpy as np
from elements.ElementLogic.dataClasses import Geometry
from shapely import geometry

geo = Geometry(name='', length=200, width=500, x_position=0, y_position=0, angle=0, height=0)


class ContainerDispositions:
    """
    For containers, length is the dimensions in the width/length axis of the shelf and width is the dimensions in the depth
    axis of the shelf
    """

    def __init__(self):
        self.dispo = []
        self.container_nb = 3
        self.containers = []

        self.sizes = np.array([500, 200])   # [big, small]

        self.h = np.array([
            [1, 0],
            [0, 1]
        ])

        print(np.matmul(self.sizes, self.h))
        rows = []
        columns = []

    def geo_dimensions(self, geo: Geometry):
        """
        returns dimensions of given geometry sorted in descending order
        :param geo:
        :return:
        """
        geometry = np.sort(geo.geometry[0])[::-1]
        return geometry

    def create_geometry(self, geometry: Geometry):
        # geometry, length is dim
        geometry = Geometry(
            name='name',
            length=23, width=23,
            x_position=0, y_position=0,
            angle=0, height=0
        )


    def make_grid_layout(self, row_count, col_count, orientation):
        length = 500
        width = 200
        group = []
        for r in range(0, row_count):
            for c in range(0, col_count):
                if orientation == 90:
                    x = width * (c + 1)
                    y = r * length
                    position = [x, y]
                    print(position)






    def rows(self):
        print('gettings rows')




e = ContainerDispositions()
# e.geo_dimensions(geo)
e.make_grid_layout(3, 2, 90)


