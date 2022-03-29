import PyQt6
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt6.QtWidgets import *
from layout.central.storeOverview.storeViewerWidget.toolBarControls import StoreViewerControls
from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.actions import *
from layout.central.storeOverview.panel.elementInspector import ElementInspector
from layout.central.storeOverview.panel.storeOverviewPanel import StoreOverviewPanel
from elements.store.dataClasses import *
from elements.elementsTypes import *
from PyQt6.QtGui import *
from elements.store.storeObject import *
from math import *
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *

class StoreOverview(QWidget):



    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        wid = QWidget()
        self.setContentsMargins(5, 5, 5, 5)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter()
        self.splitter.setHandleWidth(3)
        self.splitter.createHandle()
        print('handle', self.splitter.handle(0))
        hbox.addWidget(self.splitter)
        self.setLayout(hbox)

        # self.splitter.setMinimumSize(500, 500)
        # self.splitter.setBaseSize(400, 500)
        # self.splitter.setAutoFillBackground(True)
        # self.splitter.setBackgroundRole(QPalette.ColorRole.Base)

        self.right_splitter = QSplitter()

        self.store_visual = StoreTopVisualizer()
        self.shelf_visual = ShelfViewer()

        # self.controls = StoreViewerControls(self.store_visual)
        self.panel = StoreOverviewPanel(store_viewer=self.store_visual, shelf_viewer=self.shelf_visual)
        print('size', self.height(), self.width())

        # self.main_grid_layout = QGridLayout()
        # self.store_visual.setMinimumSize(PyQt6.QtCore.QSize(200, 400))
        self.store_visual.new_rect_signal.connect(self.handle_element_selection)
        self.store_visual.selection_signal.connect(self.handle_element_selection)
        self.store_visual.unselect_signal.connect(self.handle_unselect)

        self.splitter.addWidget(self.panel)
        self.right_splitter.addWidget(self.store_visual)
        self.right_splitter.addWidget(self.shelf_visual)
        self.right_splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.right_splitter)

        # SIGNAL FOR ACTIONS




        # self.main_grid_layout.addWidget(self.controls, 1, 1)



        # TODO: add splitter to change width
        # self.setMinimumWidth(1000)
        # self.splitter.addWidget(self.panel)
        # self.splitter.addWidget(self.store_visual)

        # self.main_grid_layout.addWidget(self.panel, 2, 1)
        # self.main_grid_layout.addWidget(self.store_visual, 1, 2, 2, 1)
        # self.setLayout(self.main_grid_layout)

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







