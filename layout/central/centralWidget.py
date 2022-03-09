from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStackedLayout
import sys
from layout.central.catalogOverview.catalogOverview import CatalogOverview
from layout.central.storeOverview.storeOverview import StoreOverview


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(10, 10, 400, 400)
        # self.setStyleSheet('background-color:blue')

        self.stackedlayout = QStackedLayout()
        self.catalog_overview = CatalogOverview()


        self.screen2 = StoreOverview()
        self.screen2.setStyleSheet('background-color:blue')
        self.screen3 = QWidget()
        self.screen3.setStyleSheet('background-color:green')

        self.create_layout()
        self.stackedlayout.setCurrentIndex(1)

    def handle_stack_change(self, index):
        if type(index) is int:
            self.stackedlayout.setCurrentIndex(index)
        else:
            if index == 'up':
                if self.stackedlayout.currentIndex() + 1 >= self.stackedlayout.count():
                    self.stackedlayout.setCurrentIndex(0)
                else:
                    self.stackedlayout.setCurrentIndex(self.stackedlayout.currentIndex() + 1)
            elif index == 'down':
                if self.stackedlayout.currentIndex() == 0:
                    self.stackedlayout.setCurrentIndex(self.stackedlayout.count() - 1)
                else:
                    self.stackedlayout.setCurrentIndex(self.stackedlayout.currentIndex() - 1)



    def create_layout(self):

        self.stackedlayout.addWidget(self.catalog_overview)
        self.stackedlayout.addWidget(self.screen2)
        self.stackedlayout.addWidget(self.screen3)
        self.setLayout(self.stackedlayout)

