from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
from layout.central.storeOverview.panel.rackingInspector.rackingInspector import RackingInspector
from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.toolBarControls import StoreViewerControls
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
from layout.central.storeOverview.shelfViewerWidget.toolBar.shelfToolBar import *


class RackingPanel(QWidget):
    def __init__(self, store_viewer: StoreTopVisualizer, shelf_viewer: ShelfViewer):
        super().__init__()
        # self.setMaximumWidth(500)
        self.main_vbox = QVBoxLayout()
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.store_viewer = store_viewer
        self.setGeometry(0, 0, 100, 100)
        self.store_viewer_controls = StoreViewerControls(store_viewer=store_viewer)
        self.racking_inspector = RackingInspector(store_viewer=self.store_viewer)
        self.main_vbox.addWidget(self.store_viewer_controls)
        self.main_vbox.addWidget(self.racking_inspector)
        self.setLayout(self.main_vbox)

