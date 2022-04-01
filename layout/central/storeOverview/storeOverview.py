from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.actions import *
from layout.central.storeOverview.panel.rackingInspector.rackingPanel import RackingPanel
from elements.store.dataClasses import *
from elements.store.storeObject import *
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
from layout.central.storeOverview.panel.shelfInspector.shelfPanel import *

class StoreOverview(QWidget):



    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setContentsMargins(5, 5, 5, 5)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter()
        hbox.addWidget(self.splitter)

        self.store_visual = StoreTopVisualizer()
        self.shelf_visual = ShelfViewer()

        self.store_visual.new_rect_signal.connect(self.handle_racking_selection)
        self.store_visual.selection_signal.connect(self.handle_racking_selection)
        self.store_visual.unselect_signal.connect(self.handle_unselect)

        self.racking_panel = RackingPanel(store_viewer=self.store_visual, shelf_viewer=self.shelf_visual)
        self.racking_panel.racking_inspector.racking_content.new_shelf_signal.connect(self.handle_shelf_creation)
        self.shelf_panel = ShelfPanel()

        self.splitter.addWidget(self.racking_panel)
        self.splitter.addWidget(self.shelf_panel)

        # self.racking_panel.racking_inspector.racking_content.new_shelf_signal.connect(self.create_shelf)
        # self.racking_panel.racking_inspector.racking_content.new_shelf_signal.connect(self.test)
        self.racking_panel.racking_inspector.racking_content.new_shelf_button.clicked.connect(self.handle_shelf_creation)

        self.right_splitter = QSplitter()
        self.right_splitter.addWidget(self.store_visual)
        self.right_splitter.addWidget(self.shelf_visual)
        self.right_splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.right_splitter)
        print('collapse', self.splitter.isCollapsible(1))
        self.splitter.setSizes([10, 100, 1000])

        self.setLayout(hbox)


    def test(self):
        print('test')

    def handle_shelf_creation(self, constructor: ElementConstructorData):
        print('handle shelf creation storeOverview')
        self.shelf_panel.shelf_inspector.update_child_information(constructor)
        self.shelf_panel.show_panel(250)



    def handle_racking_creation(self, constructor: ElementConstructorData):
        """
        Sends the ElementConstructorData to inspector
        :param constructor: elementConstructorData
        :return: void
        """
        self.racking_panel.racking_inspector.update_child_informations(constructor)

    def handle_racking_selection(self, element: StoreObject):
        if element is not None:
            self.racking_panel.racking_inspector.update_child_informations(element)



    def handle_unselect(self):
        print('handle unselect')
        self.racking_panel.racking_inspector.update_child_informations(None)


        self.shelf_panel.setMinimumWidth(0)
        self.shelf_panel.setMaximumWidth(0)

    def create_shelf(self, a0):
        print('new shelf')
        print(a0)







