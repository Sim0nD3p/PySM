from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
from layout.central.storeOverview.panel.rackingPanel.rackingInspector import RackingInspector
from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.toolBarControls import StoreViewerControls
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
from layout.central.storeOverview.shelfViewerWidget.toolBar.shelfToolBar import *
from layout.central.storeOverview.panel.panel import *


class RackingPanel(Panel):
    """
    Racking panel, contains rackingPanel
    TODO: should add submit/cancel buttons directly in racking panel
    """
    def __init__(self, store_viewer: StoreTopVisualizer, shelf_viewer: ShelfViewer):
        super().__init__()
        self.store_viewer = store_viewer
        self.racking_tool_bar = StoreViewerControls(store_viewer=store_viewer)
        self.racking_inspector = RackingInspector(store_viewer=self.store_viewer)
        self.set_tool_bar(self.racking_tool_bar)
        self.set_inspector(self.racking_inspector)

        self.submit_button.clicked.connect(self.handle_submit)
        self.cancel_button.clicked.connect(self.handle_cancel)

    def handle_submit(self):
        print('handle submit rackingPanel')
        self.racking_inspector.handle_submit()

    def handle_cancel(self):
        print('handle cancel')


