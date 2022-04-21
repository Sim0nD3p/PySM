from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from elements.shelf.shelf import *
from elements.shelf.flatShelf import *
from backend.ContainerCatalog import *
from layout.components.dimensionsSelector import *
from elements.ElementLogic.StorageObject import *
from backend.storeFloor import *


class ContainerSelector(QWidget):
    """
    Selects the container
    """
    container_change = pyqtSignal(type, int, int, int, name='container_change')

    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()
        self.main_vbox.setContentsMargins(0, 0, 0, 0)

        # label container selector
        self.main_vbox.addSpacing(10)
        label_cont_select = QLabel('Choix contenant')
        self.main_vbox.addWidget(label_cont_select)

        # type contenant
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        type_label = QLabel('Type de contenant:')
        self.type_cb = QComboBox()
        self.type_cb.currentIndexChanged.connect(self.handle_type_change)
        hbox.addWidget(type_label)
        hbox.addWidget(self.type_cb)
        self.main_vbox.addLayout(hbox)

        # subtype contentant
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        cont_label = QLabel('Contenant: ')
        self.subtype_cb = QComboBox()
        hbox.addWidget(cont_label)
        hbox.addWidget(self.subtype_cb)
        self.main_vbox.addLayout(hbox)

        self.subtype_cb.currentIndexChanged.connect(self.handle_subtype_change)

        self.dimensions_selector = DimensionSelector()
        self.dimensions_selector.dimensions_change.connect(self.handle_dimensions_change)
        self.main_vbox.addWidget(self.dimensions_selector)



        self.setLayout(self.main_vbox)


    def draw_type_cb(self, element: Shelf):
        """
        Draws the type combobox for compatible container fo a given shelving
        :param element: Shelf
        :return:
        """

        self.type_cb.clear()    # problem seems to be here, makes app crash, triggers valueChange
        if issubclass(type(element), Shelf):
            if element.compatible_containers:
                for container in element.compatible_containers:
                    self.type_cb.addItem(container.display_type, container)

    def draw_subtype_cb(self):
        print('containerSelector - draw subtype_cb according to type selected by default for selected group')

    def handle_type_change(self, type_cb_index):
        """
        Handles ComboBox for subtypes according to type selected in type comboBox
        :param type_cb_index: index of type ComboBox
        :return:
        """
        print('handling main cb change')
        if type_cb_index != -1:
            print('type_cb_index', type_cb_index)
            container_type = self.type_cb.itemData(type_cb_index)
            subtypes = ContainerCatalog().get_containers(container_type=container_type)
            self.subtype_cb.clear()

            if len(subtypes) == 0:
                self.subtype_cb.setDisabled(True)
            else:
                self.subtype_cb.setDisabled(False)
                for subtype in subtypes:
                    self.subtype_cb.addItem(subtype.name, subtype)




    def handle_subtype_change(self, subtype_cb_index):
        if subtype_cb_index != -1:
            subtype = self.subtype_cb.itemData(subtype_cb_index)
            if issubclass(type(subtype), Container):
                self.dimensions_selector.setDisabled(True)
                # print(subtype)
                # print(subtype.length(), subtype.width(), subtype.height())

                self.dimensions_selector.set_dimensions(length=subtype.length(),
                                                        width=subtype.width(),
                                                        height=subtype.height()
                                                        )

        elif self.type_cb.currentIndex() != -1:
            self.dimensions_selector.set_dimensions(length=0,
                                                    width=0,
                                                    height=0
                                                    )
            self.dimensions_selector.setDisabled(False)
            # self.container_change.emit(subtype, 12, 12, 12)

    def handle_dimensions_change(self):
        """
        Called when dimensions change signal is emitted from dimensions widget
        :return:
        """
        length = self.dimensions_selector.length()
        width = self.dimensions_selector.width()
        height = self.dimensions_selector.height()
        if self.type_cb.currentIndex() != -1:
            container = self.type_cb.itemData(self.type_cb.currentIndex())
            self.container_change.emit(container, length, width, height)



    def get_container(self):
        """
        Gets the selected container and its dimensions
        :return:
        """
        container = None
        if self.type_cb.currentIndex() != -1:
            container_type = self.type_cb.itemData(self.type_cb.currentIndex())
            if len(ContainerCatalog.get_containers(container_type=container_type)) == 0:
                container = container_type
            else:
                container = self.subtype_cb.itemData(self.subtype_cb.currentIndex())
        return container



    def display_blank(self):
        """
        Display blank values for all input elements
        :return:
        """
        self.type_cb.clear()
        self.subtype_cb.clear()
        self.dimensions_selector.set_dimensions(0, 0, 0)








    def update_information(self, element: StorageObject):
        """
        Updates informations to display good information on the selection part of the widget to select container
        according to shelf
        could be simplified
        :param element:
        :return:
        """
        if hasattr(element, 'parent_shelf_id'):
            shelf_target = StoreFloor.get_shelf_by_id(element.parent_shelf_id)
            self.draw_type_cb(shelf_target)
            self.draw_subtype_cb()
            print('test3')
        else:
            self.display_blank()



