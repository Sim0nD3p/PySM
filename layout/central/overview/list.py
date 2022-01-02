from PyQt6.QtWidgets import QListWidget, QLabel, QPushButton, QWidget, QHBoxLayout, QListWidgetItem
from backend.PartCatalog import PartCatalog

class ListWidget(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self.itemClicked.connect(self.handle_selection)
        self.part_catalog = PartCatalog()

    def draw_list(self, list):
        for item in list:
            if type(item) == str:
                row = QListWidgetItem(item)
            else:
                row = QListWidgetItem(item.code)

            self.addItem(row)

    def handle_selection(self, element):
        print('hello')
        e = self.part_catalog.get_part(element.text())
        print(e.__dict__)


