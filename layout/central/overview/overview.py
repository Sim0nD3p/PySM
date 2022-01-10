from PyQt6.QtWidgets import QWidget, QListWidget, QGridLayout, QVBoxLayout, QHBoxLayout
from layout.central.overview.list import ListWidget
from layout.central.overview.treeWidget import TreeWidget

class Overview(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout()
        hbox = QHBoxLayout()

        self.sub1 = QWidget()
        self.sub1.setStyleSheet('background-color:yellow')
        self.sub1.setMinimumWidth(800)
        self.sub1.setMinimumHeight(400)

        self.tree_widget = TreeWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.tree_widget)
        self.sub1.setLayout(vbox)

        list = ['item1', 'item2', 'item3']
        self.list_widget = ListWidget(self)
        self.list_widget.draw_list(list)

        self.sub3 = QWidget()
        self.sub3.setStyleSheet('background-color:green')
        self.sub3.setMinimumWidth(500)
        self.sub3.setMinimumHeight(200)

        self.grid_layout.addWidget(self.sub3, 0, 0)
        self.grid_layout.addWidget(self.list_widget, 1, 0)
        self.grid_layout.addWidget(self.sub1, 0, 1, 2, 1)
        self.setLayout(self.grid_layout)

    def handle_list_change(self, element):
        print('handle list change')
        print(element)
        self.tree_widget.draw_tree(element)
