from PyQt6.QtWidgets import QWidget, QListWidget, QGridLayout, QVBoxLayout
from layout.central.overview.listView import ListWidget

class Overview(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout()

        self.sub1 = QWidget()
        self.sub1.setStyleSheet('background-color:yellow')

        self.list_widget = ListWidget()
        # self.sub2.setStyleSheet('background-color:grey')

        self.sub3 = QWidget()
        self.sub3.setStyleSheet('background-color:green')

        self.sub4 = QWidget()
        self.sub4.setStyleSheet('background-color:orange')

        vbox = QVBoxLayout()
        vbox.addWidget(self.sub1)
        vbox.addWidget(self.list_widget)

        self.grid_layout.addWidget(self.sub3, 0, 0)
        self.grid_layout.addWidget(self.sub4, 1, 0)
        self.grid_layout.addLayout(vbox, 0, 1, 2, 1)
        self.setLayout(self.grid_layout)



