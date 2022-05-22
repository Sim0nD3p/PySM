from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton

from elements.racking.racking import Racking
from layout.central.storeOverview.panel.rackingPanel.rackingInspector import RackingInspector
from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.toolBarControls import StoreViewerControls
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
from layout.central.storeOverview.shelfViewerWidget.toolBar.shelfToolBar import *
from layout.central.storeOverview.panel.panel import *
from copy import deepcopy


class RackingPanel(Panel):
    """
    Racking panel, contains rackingPanel
    TODO: should add submit/cancel buttons directly in racking panel
    """
    def __init__(self, store_viewer: StoreTopVisualizer, shelf_viewer: ShelfViewer):
        super().__init__()
        self.store_viewer = store_viewer
        self.setMaximumWidth(400)
        self.element_copy = None    # used for restoring element on cancel
        self.show_panel(175)
        self.racking_tool_bar = StoreViewerControls(store_viewer=store_viewer)
        self.racking_inspector = RackingInspector(store_viewer=self.store_viewer)
        self.set_tool_bar(self.racking_tool_bar)
        self.set_inspector(self.racking_inspector)

        self.submit_button.clicked.connect(self.handle_submit)
        self.cancel_button.clicked.connect(self.handle_cancel)
        self.delete_button.clicked.connect(self.handle_delete)

        self.disable_buttons()

    def update_informations(self, element):
        if issubclass(type(element), Racking):
            self.element_copy = deepcopy(element)
            print('lets go')
            self.show_panel(175)
            self.enable_buttons()
            self.racking_inspector.update_child_informations(element)



    def handle_submit(self):
        print('handle submit rackingPanel')
        self.racking_inspector.handle_submit()
        self.disable_buttons()
        # TODO: immidiately update shelf inspector (panel) when submitting (if active shelf)

    def handle_cancel(self):
        print('handle cancel')
        if hasattr(self.racking_inspector.element, 'id'):

            for obj in StoreFloor.objects:
                if hasattr(obj, 'id') and obj.id == self.racking_inspector.element.id:
                    # find the element in store and replace it with backup element
                    StoreFloor.delete_store_object(object_id=self.racking_inspector.element.id)
                    StoreFloor.add_object(self.element_copy)
                    self.racking_inspector.unselect_signal.emit()   # kinda wak but signal works

    def handle_delete(self):
        print('handling delete from rackingPanel')
        self.racking_inspector.handle_delete()



