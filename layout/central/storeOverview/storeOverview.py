import PyQt6.QtCore
from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout
from layout.central.storeOverview.physicalViewer.toolBarControls import StoreViewerControls
from layout.central.storeOverview.physicalViewer.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.physicalViewer.actions import *
from layout.central.storeOverview.panel.elementInspector import ElementInspector
from layout.central.storeOverview.panel.storeOverviewPanel import StoreOverviewPanel
from elements.store.dataClasses import *
from math import *

class StoreOverview(QWidget):
    def __init__(self):
        super().__init__()
        self.main_grid_layout = QGridLayout()
        self.store_visual = StoreTopVisualizer()
        self.store_visual.setMinimumSize(PyQt6.QtCore.QSize(200, 400))
        self.store_visual.new_rect_signal.connect(self.handle_element_creation)

        # self.controls = StoreViewerControls(self.store_visual)


        # self.main_grid_layout.addWidget(self.controls, 1, 1)


        # TODO: add splitter to change width
        # self.splitter = QSplitter()
        self.panel = StoreOverviewPanel(store_viewer=self.store_visual)

        self.main_grid_layout.addWidget(self.panel, 2, 1)
        self.main_grid_layout.addWidget(self.store_visual, 1, 2, 2, 1)
        self.setLayout(self.main_grid_layout)


    def handle_element_creation(self, c1: QPointF, c2: QPointF):
        print('handle new rect')
        minx = min([c1.x(), c2.x()])
        maxx = max([c1.x(), c2.x()])
        print('min max', minx, maxx)

        miny = min([c1.y(), c2.y()])
        maxy = max([c1.y(), c2.y()])
        print('min max y', miny, maxy)

        x_position = minx
        y_position = miny

        dx = maxx - minx
        dy = maxy - minx

        if dx > dy:
            length = dx
            width = dy
            angle = 0
        else:
            length = dy
            width = dx
            angle = 90

        constructor = ElementConstructorData(
            x_position=x_position,
            y_position=y_position,
            length=length,
            width=width,
            angle=angle,
            height=0
        )
        self.panel.element_inspector.update_child_informations(constructor)

        print(minx)





