from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QTabWidget
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt
from layout.central.storeOverview.panel.rackingInformations.rackingProperties import RackingProperties


class RackingCard(QTabWidget):
    def __init__(self):
        super().__init__()
        self.racking_properties = RackingProperties()
        self.addTab(self.racking_properties, 'Informations générales')

    def update_child_informations(self, racking):
        self.racking_properties.update_informations(racking)