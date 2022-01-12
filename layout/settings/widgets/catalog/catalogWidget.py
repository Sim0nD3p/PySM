from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSpacerItem
from backend.PartCatalog import PartCatalog

"""
    Main file for catalog
    
    
"""

class CatalogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_layout()

    def create_layout(self):
        vbox = QVBoxLayout()
        b_print_catalog = QPushButton('print catalog')
        b_print_catalog.clicked.connect(self.print_catalog)
        vbox.addWidget(b_print_catalog)

        self.setLayout(vbox)

    def print_catalog(self):
        PartCatalog.print_catalog()
