from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.central.storeOverview.panel.panel import *
from elements.elementsTypes import *
from elements.container.container import *


class ContainerPanel(Panel):
    def __init__(self):
        super().__init__()
        self.hide_panel()
