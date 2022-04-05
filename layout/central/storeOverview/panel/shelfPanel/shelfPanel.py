from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from layout.central.storeOverview.panel.shelfPanel.shelfInspector import *
from elements.store.dataClasses import ElementConstructorData


class ShelfPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.setMinimumWidth(0)
        self.setMaximumWidth(0)
        self.main_vbox = QVBoxLayout()

        self.cancel_bt = QPushButton('Cancel')
        self.submit_bt = QPushButton('Ok')
        self.cancel_bt.clicked.connect(self.handle_cancel)
        self.submit_bt.clicked.connect(self.handle_submit)

        but_hb = QHBoxLayout()
        but_hb.addSpacing(100)
        but_hb.addWidget(self.cancel_bt)
        but_hb.addWidget(self.submit_bt)


        self.shelf_inspector = ShelfInspector()

        self.main_vbox.addWidget(self.shelf_inspector)
        self.main_vbox.addLayout(but_hb)

        self.setLayout(self.main_vbox)

    def handle_submit(self):
        """
        Hides panel and handle submit by calling inspector' method
        :return:
        """
        self.shelf_inspector.handle_submit()
        self.hide_panel()

    def handle_cancel(self):
        self.hide_panel()

    def show_panel(self, width):
        """
        Shows shelf panel
        :param width: width (int)
        :return: void
        """
        if not width:
            width = 250

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    def hide_panel(self):
        """
        Hides panel
        :return: void
        """
        self.setMaximumWidth(0)
        self.setMinimumWidth(0)



