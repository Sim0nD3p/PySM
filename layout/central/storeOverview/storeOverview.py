from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.actions import *
from layout.central.storeOverview.panel.rackingPanel.rackingPanel import RackingPanel
from elements.store.dataClasses import *
from elements.store.storeObject import *
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
from layout.central.storeOverview.panel.shelfPanel.shelfPanel import *
from layout.central.storeOverview.panel.containerPanel.containerPanel import *
from elements.shelf.shelf import *

class StoreOverview(QWidget):
    """
    Store Overview, interface between user and store
    """



    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setContentsMargins(5, 5, 5, 5)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter()     # main splitter for viewer and panels
        hbox.addWidget(self.splitter)

        self.store_visual = StoreTopVisualizer()    # storeTopVisualiser
        self.shelf_visual = ShelfViewer()           # shelf viewer

        # signals for store viewer (new, select, unselect)
        self.store_visual.new_rect_signal.connect(self.handle_racking_selection)
        self.store_visual.selection_signal.connect(self.handle_racking_selection)
        self.store_visual.unselect_signal.connect(self.handle_unselect)


        self.racking_panel = RackingPanel(store_viewer=self.store_visual, shelf_viewer=self.shelf_visual)
        self.shelf_panel = ShelfPanel()
        self.container_panel = ContainerPanel()

        # interfaces with racking inspector
        self.racking_panel.racking_inspector.racking_content.new_shelf_signal.connect(self.handle_shelf_creation)
        self.racking_panel.racking_inspector.racking_content.shelf_selection_signal.connect(self.handle_shelf_selection)
        self.racking_panel.racking_inspector.racking_content.new_shelf_button.clicked.connect(self.handle_shelf_creation)

        # interfaces shelf panel
        self.shelf_panel.shelf_inspector.new_shelf_signal.connect(self.racking_panel.racking_inspector.racking_content.
                                                                  draw_list)

        self.splitter.addWidget(self.racking_panel)
        self.splitter.addWidget(self.shelf_panel)
        self.splitter.addWidget(self.container_panel)



        self.right_splitter = QSplitter()       # viewer splitter
        self.right_splitter.addWidget(self.store_visual)
        self.right_splitter.addWidget(self.shelf_visual)
        self.right_splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.right_splitter)
        self.splitter.setSizes([10, 100, 100, 1000])

        self.setLayout(hbox)


    def test(self):
        print('test')

    def handle_shelf_creation(self, constructor: ElementConstructorData):
        print('handle shelf creation storeOverview')
        self.shelf_panel.shelf_inspector.update_child_information(constructor)
        self.shelf_panel.show_panel(300)

    def handle_shelf_selection(self, shelf: Shelf):
        print('handle shelf selection')
        self.shelf_panel.shelf_inspector.update_child_information(shelf)
        self.shelf_panel.show_panel(300)


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
            self.shelf_panel.shelf_inspector.set_parent_racking(element)



    def handle_unselect(self):
        print('handle unselect')
        self.racking_panel.racking_inspector.update_child_informations(None)


        self.shelf_panel.setMinimumWidth(0)
        self.shelf_panel.setMaximumWidth(0)









