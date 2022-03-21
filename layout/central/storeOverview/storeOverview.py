import PyQt6
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout
from layout.central.storeOverview.physicalViewer.toolBarControls import StoreViewerControls
from layout.central.storeOverview.physicalViewer.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.physicalViewer.actions import *
from layout.central.storeOverview.panel.elementInspector import ElementInspector
from layout.central.storeOverview.panel.storeOverviewPanel import StoreOverviewPanel
from elements.store.dataClasses import *
from elements.elementsTypes import *
from elements.store.storeObject import *
from math import *

class StoreOverview(QWidget):



    def __init__(self):
        super().__init__()
        self.main_grid_layout = QGridLayout()
        self.store_visual = StoreTopVisualizer()
        self.store_visual.setMinimumSize(PyQt6.QtCore.QSize(200, 400))
        self.store_visual.new_rect_signal.connect(self.handle_element_selection)
        self.store_visual.selection_signal.connect(self.handle_element_selection)
        self.store_visual.unselect_signal.connect(self.handle_unselect)

        # self.controls = StoreViewerControls(self.store_visual)


        # self.main_grid_layout.addWidget(self.controls, 1, 1)


        # TODO: add splitter to change width
        # self.splitter = QSplitter()
        self.panel = StoreOverviewPanel(store_viewer=self.store_visual)

        self.main_grid_layout.addWidget(self.panel, 2, 1)
        self.main_grid_layout.addWidget(self.store_visual, 1, 2, 2, 1)
        self.setLayout(self.main_grid_layout)

    def handle_element_creation(self, constructor: ElementConstructorData):
        """
        Sends the ElementConstructorData to inspector
        :param constructor: elementConstructorData
        :return: void
        """
        self.panel.element_inspector.update_child_informations(constructor)

    def handle_element_selection(self, element: StoreObject):
        if element is not None:
            self.panel.element_inspector.update_child_informations(element)


    def handle_unselect(self):
        self.panel.element_inspector.update_child_informations(None)







