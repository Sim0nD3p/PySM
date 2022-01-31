from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedLayout, QLineEdit, QLabel, QPushButton
from layout.importer.xmlImporter import XmlImporter
from layout.importer.jsonImporter import JsonImporter
from layout.importer.new_parts.part_importer import PartImporter

class Test(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel('dafs', self)

    def test(self):
        print('test')

class PropsPusher(QWidget):
    def __init__(self):
        super().__init__()
