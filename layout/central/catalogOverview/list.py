from PyQt6.QtWidgets import QListWidget, QLabel, QPushButton, QWidget, QHBoxLayout, QListWidgetItem
from backend.PartCatalog import PartCatalog

class ListWidget(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.itemClicked.connect(self.handle_selection)
        self.part_catalog = PartCatalog()

    def draw_list(self, list):
        """

        :param list: list of string or list of parts
        :return:
        """
        self.clear()
        for item in list:
            if type(item) == str:
                row = QListWidgetItem(item)
            else:
                row = QListWidgetItem(item.code)

            self.addItem(row)

    def handle_selection(self, element):
        e = self.part_catalog.get_part(element.text())
        self.parent.handle_list_change(e)



