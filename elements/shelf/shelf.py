from layout.settings.settings import *
import numpy as np

"""
Multiple shelves style:
- flat
"""
content_height = 0
net_height = Settings.default_shelf_net_height


class Shelf:
    """
    Parent class for shelf
    What should shelf do exactly
    """
    def __init__(self, name, element_type, shelf_length, shelf_width, shelf_height):
        self.name = name
        self.type = element_type
        self.geometry_matrix = np.array([
            [shelf_length, shelf_width],
            [shelf_height, net_height]
        ])
        self.content = []

    def content_height(self):
        content_matrix = np.array([])

        for element in self.content:
            np.append(content_matrix, element.geometry[2, 1])

