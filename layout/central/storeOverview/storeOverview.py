import PyQt6.QtCore
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout
from layout.central.storeOverview.physicalViewer.toolBarControls import StoreViewerControls
from layout.central.storeOverview.physicalViewer.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.physicalViewer.actions import *
from layout.central.storeOverview.panel.rackingCard import RackingCard
from layout.central.storeOverview.panel.storeOverviewPanel import StoreOverviewPanel

class StoreOverview(QWidget):
    def __init__(self):
        super().__init__()
        self.main_grid_layout = QGridLayout()
        self.store_visual = StoreTopVisualizer()
        self.store_visual.setMinimumSize(PyQt6.QtCore.QSize(200, 400))

        # self.controls = StoreViewerControls(self.store_visual)

        # self.main_grid_layout.addWidget(self.controls, 1, 1)


        # TODO: add splitter to change width
        # self.splitter = QSplitter()

        left = StoreOverviewPanel(store_viewer=self.store_visual)
        #vbox = QVBoxLayout()


        # b_add = QPushButton('+')
        # vbox.addWidget(b_add)

        # b_test = QPushButton('button test')
        # vbox.addWidget(b_test)

        # b_move_vp = QPushButton('move viewport')
        # b_move_vp.clicked.connect(lambda: self.store_visual.move_offset(0, 10))
        # vbox.addWidget(b_move_vp)

        # left.setLayout(vbox)
        # b_add.clicked.connect(self.store_visual.draw_shape)

        self.main_grid_layout.addWidget(left, 2, 1)
        self.main_grid_layout.addWidget(self.store_visual, 1, 2, 2, 1)
        self.setLayout(self.main_grid_layout)

    def test(self):
        print('this is second test')



