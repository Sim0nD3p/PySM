from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

"""
    Main file for catalog
    
    
"""

class CatalogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: blue')
        self.button = QPushButton('click me', self)

        self.catalog_file_name = QLabel('nom du fichier catalogue')
        self.catalog_file = QWidget(self)
        self.draw_catalog_file()

    def draw_catalog_file(self):
        hbox = QHBoxLayout()

        label = QLabel('Fichier catalogue:')

        hbox.addWidget(label)
        hbox.addWidget(self.catalog_file_name)

        self.catalog_file.setLayout(hbox)
