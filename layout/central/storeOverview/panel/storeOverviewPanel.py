from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from layout.central.storeOverview.panel.elementInspector import ElementInspector
from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.toolBarControls import StoreViewerControls
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
import math

class StoreOverviewPanel(QWidget):
    def __init__(self, store_viewer: StoreTopVisualizer, shelf_viewer: ShelfViewer):
        super().__init__()
        # self.setMaximumWidth(500)
        self.main_vbox = QVBoxLayout()
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.store_viewer = store_viewer

        self.store_viewer_controls = StoreViewerControls(store_viewer=store_viewer, shelf_viewer=shelf_viewer)
        self.element_inspector = ElementInspector(store_viewer=self.store_viewer)


        self.main_vbox.addWidget(self.store_viewer_controls)
        self.main_vbox.addWidget(self.element_inspector)

        # buttons for testing
        hbox = QHBoxLayout()
        but = QPushButton('test1')
        # but.clicked.connect(self.sv.draw_shape)
        hbox.addWidget(but)

        self.main_vbox.addLayout(hbox)

        self.setLayout(self.main_vbox)

