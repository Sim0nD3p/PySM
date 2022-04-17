from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.central.storeOverview.panel.panel import *
from elements.elementsTypes import *
from elements.container.container import *
from layout.central.storeOverview.panel.containerPanel.containerInspector import *


class ContainerPanel(Panel):
    def __init__(self):
        super().__init__()
        self.hide_panel()

        self.container_inspector = ContainerInspector()
        self.set_inspector(self.container_inspector)
        self.submit_button.clicked.connect(self.handle_submit)


    def handle_submit(self):
        self.container_inspector.handle_submit()

