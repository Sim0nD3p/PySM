from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.panel.shelfPanel.shelfInspector import *
from elements.store.dataClasses import ElementConstructorData
from layout.central.storeOverview.panel.panel import *


class ShelfPanel(Panel):

    def __init__(self):
        super().__init__()

        self.shelf_inspector = ShelfInspector()
        self.set_inspector(self.shelf_inspector)

        self.submit_button.clicked.connect(self.handle_submit)
        self.hide_panel()


    def handle_submit(self):
        """
        Hides panel and handle submit by calling inspector' method
        :return:
        """
        self.shelf_inspector.handle_submit()
        self.hide_panel()

    def handle_cancel(self):
        self.hide_panel()


