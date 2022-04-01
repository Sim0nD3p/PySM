from elements.shelf.shelf import Shelf


class FlatShelf(Shelf):
    def __init__(self, name, length, width, height):
        super().__init__(name=name, shelf_length=length, shelf_width=width, shelf_height=height)
