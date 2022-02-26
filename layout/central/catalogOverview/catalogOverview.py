from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QListWidget, QGridLayout, QVBoxLayout, QHBoxLayout
from layout.central.catalogOverview.list import ListWidget
from layout.central.catalogOverview.treeWidget import TreeWidget
from PyQt6.QtGui import QShortcut, QKeySequence
from layout.central.catalogOverview.filterWidget import FilterWidget
from backend.PartCatalog import PartCatalog

class CatalogOverview(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout()
        hbox = QHBoxLayout()
        self.filter_widget = FilterWidget()

        self.search_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.search_shortcut.activated.connect(self.handle_catalog_search)

        self.rightPanel = QWidget()
        self.rightPanel.setMinimumWidth(800)
        self.rightPanel.setMinimumHeight(400)
        self.rightPanel.setStyleSheet('background-color:red')


        self.right_vbox = QVBoxLayout()
        self.tree_widget = TreeWidget()
        self.create_right_panel()


        self.rightPanel.setLayout(self.right_vbox)

        list = ['item1', 'item2', 'item3']
        self.list_widget = ListWidget(self)
        self.list_widget.draw_list(list)


        self.filter_widget.b_submit_search.clicked.connect(self.handle_catalog_search)
        # self.filter_widget.setStyleSheet('background-color:red')
        # self.sub3.setStyleSheet('background-color:green')
        self.filter_widget.setMinimumWidth(500)
        self.filter_widget.setMinimumHeight(200)

        self.grid_layout.addWidget(self.filter_widget, 0, 0)
        self.grid_layout.addWidget(self.list_widget, 1, 0)
        self.grid_layout.addWidget(self.rightPanel, 0, 1, 2, 1)
        self.setLayout(self.grid_layout)


    def create_right_panel(self):
        self.right_vbox.setContentsMargins(0, 0, 0, 0)
        self.right_vbox.addWidget(self.tree_widget)

    def update_catalog_overview_features(self):
        self.list_widget.draw_list(PartCatalog.catalog)
        self.filter_widget.update_types_dropdown()

    def handle_catalog_search(self):
        filtered_list = self.filter_widget.filter_catalog()
        self.list_widget.draw_list(filtered_list)



    def handle_list_change(self, element):
        self.tree_widget.draw_tree(element)


    def test(self):
        print('test')

