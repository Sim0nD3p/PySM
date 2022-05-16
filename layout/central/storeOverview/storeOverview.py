from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.storeViewerWidget.actions import *
from layout.central.storeOverview.panel.rackingPanel.rackingPanel import RackingPanel
from elements.store.dataClasses import *
from elements.store.storeObject import *
from layout.central.storeOverview.shelfViewerWidget.shelfViewer import *
from layout.central.storeOverview.panel.shelfPanel.shelfPanel import *
from layout.central.storeOverview.panel.containerPanel.containerPanel import *
from elements.shelf.shelf import *
import copy

class StoreOverview(QWidget):
    """
    Store Overview, interface between user and store
    """



    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setContentsMargins(5, 5, 5, 5)
        # self.setMaximumHeight(500)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter()     # main splitter for viewer and panels
        hbox.addWidget(self.splitter)

        self.store_visual = StoreTopVisualizer()    # storeTopVisualiser
        self.shelf_visual = ShelfViewer()           # shelf viewer

        # signals for store viewer (new, select, unselect)
        self.store_visual.new_rect_signal.connect(self.handle_racking_creation)
        self.store_visual.selection_signal.connect(self.handle_racking_selection)
        self.store_visual.unselect_signal.connect(self.unselect_all)


        self.racking_panel = RackingPanel(store_viewer=self.store_visual, shelf_viewer=self.shelf_visual)
        self.shelf_panel = ShelfPanel()
        self.container_panel = ContainerPanel()


        #Actions signals
        self.racking_panel.racking_tool_bar.delete.delete_signal.connect(self.unselect_all)

        # interfaces with racking inspector
        self.racking_panel.racking_inspector.new_shelf_signal.connect(self.handle_shelf_creation)
        self.racking_panel.racking_inspector.racking_content.shelf_selection_signal.connect(self.handle_shelf_selection)
        self.racking_panel.racking_inspector.unselect_signal.connect(self.unselect_all)
        self.racking_panel.racking_inspector.racking_content.new_shelf_button.clicked.connect(self.handle_shelf_creation)

        # interfaces shelf panel
        self.shelf_panel.shelf_inspector.shelf_list_update_signal.connect(self.racking_panel.racking_inspector
                                                                          .racking_content.draw_list)
        self.shelf_panel.shelf_inspector.container_select_signal.connect(self.handle_container_creation)

        # container interface (shelf)
        self.container_panel.container_inspector.container_list_update_signal.connect(self.shelf_panel.shelf_inspector
                                                                                      .update_content_list)
        self.container_panel.container_inspector.shelf_draw_signal.connect(self.draw_shelf)
        self.splitter.addWidget(self.racking_panel)
        self.splitter.addWidget(self.shelf_panel)
        self.splitter.addWidget(self.container_panel)



        self.right_splitter = QSplitter()       # viewer splitter
        self.right_splitter.addWidget(self.store_visual)
        self.right_splitter.addWidget(self.shelf_visual)
        self.right_splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.right_splitter)
        # self.splitter.setSizes([10, 100, 100, 1000])
        self.right_splitter.setSizes([100, 50])

        self.setLayout(hbox)


    def test(self):
        print('test')

    def handle_container_creation(self, storage_object):
        """
        Called when container creation/selection signal is emitted from shelfInspector
        :param storage_object:
        :return:
        """
        if issubclass(type(storage_object), StorageObject):
            # TODO deep copy for cancel operation, operations will directly affect current object
            # TODO cancel restore the deep copy
            # TODO modifications in real time for new storage_objects
            # TODO hide or display blank containerInspector on submit
            # TODO add support for 3, 5, 5, 6 containers
            # TODO add containerStack support
            self.container_panel.container_inspector.update_information(storage_object)
            self.container_panel.show_panel(300)

    def handle_container_selection(self, storage_object: StorageObject):

        # s = copy.deepcopy(storage_object)
        # print('deep copy', s)
        self.container_panel.container_inspector.update_information(storage_object)
        self.container_panel.show_panel(300)




    def handle_shelf_creation(self, constructor: ElementConstructorData):
        """
        Sends constructor to shelfInspector
        :param constructor:
        :return:
        """
        print('handle shelf creation storeOverview')
        self.shelf_panel.shelf_inspector.update_child_information(constructor)
        self.shelf_panel.show_panel(300)

    def handle_shelf_selection(self, shelf: Shelf):
        """
        Handling shelf selection calling methods in
        :param shelf:
        :return:
        """
        self.shelf_panel.shelf_inspector.update_child_information(shelf)
        self.shelf_panel.show_panel(200)
        self.shelf_visual.paint_shelf(shelf)


    def handle_racking_creation(self, constructor: ElementConstructorData):
        """
        Sends the ElementConstructorData to inspector
        :param constructor: elementConstructorData
        :return: void
        """
        print('handle racking creation')
        self.racking_panel.enable_buttons()
        self.racking_panel.racking_inspector.update_child_informations(constructor)

    def handle_racking_selection(self, element: StoreObject):
        """
        Handles racking selection, could be in rackingPanel with common method for new and existing racking
        :param element:
        :return:
        """
        if element is not None:
            self.racking_panel.enable_buttons()
            self.racking_panel.racking_inspector.update_child_informations(element)
            self.shelf_panel.shelf_inspector.set_parent_racking(element)

    def unselect_all(self):
        """
        unselect all elements
        :return:
        """
        # TODO shelfInspector unselect and shelfViewer unselect
        print('unselect all')
        self.racking_panel.disable_buttons()        # should change to better method in rackingPanel
        self.racking_panel.racking_inspector.update_child_informations(None)
        self.store_visual.selected_element = None
        self.shelf_panel.shelf_inspector.update_child_information(None)
        self.store_visual.unselect_all()
        self.store_visual.paintGL()

    def draw_shelf(self):
        print('drawing shelf')
        self.shelf_visual.paintGL()









