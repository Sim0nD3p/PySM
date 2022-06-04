from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import pyqtSignal

from layout.central.storeOverview.panel.rackingPanel.inspectorChildrens.rackingContent import RackingContent
from layout.central.storeOverview.panel.rackingPanel.inspectorChildrens.rackingProperties import RackingProperties
from layout.central.storeOverview.storeViewerWidget.storeOverallTopView import StoreTopVisualizer
from elements.store.dataClasses import *
from elements.elementsTypes import *
from elements.store.storeObject import StoreObject
from elements.racking.racking import Racking
from backend.storeFloor import StoreFloor
from elements.ElementLogic.dataClasses import *
from layout.central.storeOverview.rackingViewer.rackingViewer import *

class RackingInspector(QTabWidget):
    """
    Interface between racking and backend (racking in StoreFloor), to manage racking by user
    TODO: change submit signal to buttons in RackingInspector directly
    """
    submit_signal = pyqtSignal(str)     # changed for new_element
    new_element_signal = pyqtSignal(ElementConstructorData)     # create new element
    new_shelf_signal = pyqtSignal(ElementConstructorData, name='new_shelf')
    unselect_signal = pyqtSignal(name='unselect')


    def __init__(self, store_viewer: StoreTopVisualizer):
        super().__init__()
        self.store_viewer = store_viewer
        self.racking_properties = RackingProperties(submit_signal=self.submit_signal,
                                                    new_element_signal=self.new_element_signal)
        self.addTab(self.racking_properties, 'Propriétés')

        self.racking_content = RackingContent()
        self.addTab(self.racking_content, 'Contenu')

        self.racking_viewer = RackingViewer()
        self.addTab(self.racking_viewer, 'Racking')


        self.racking_content.new_shelf_button.clicked.connect(self.new_shelf_creation)
        self.element = Racking(name='', length=0, width=0, height=0, angle=0, id=0, x_position=0, y_position=0)
        self.submit_signal.connect(self.handle_submit)
        self.new_element_signal.connect(self.create_racking)
        self.racking_properties.geometry_change_signal.connect(self.handle_geometry_change)


    def handle_geometry_change(self, geometry: Geometry):
        """
        Handles geometry changes, connected to geometry_change_signal from racking_properties
        change the geometry of the currently selected racking element
        :param geometry:
        :return:
        """
        if self.element:
            self.element.set_length(geometry.length())
            self.element.set_width(geometry.width())
            self.element.set_x_position(geometry.x_position())
            self.element.set_y_position(geometry.y_position())
            self.element.set_height(geometry.height())
            self.element.set_angle(geometry.angle())
            self.store_viewer.paintGL()


    def handle_submit(self):
        """
        Called when submit button is clicked
        calls whether to create racking or modify the object
        :return:
        """
        if not self.element or not StoreFloor.get_id_object(self.element.id):

            print('create racking')
            self.create_racking()
        else:
            print('modify racking')
            self.racking_properties.modify_store_object()

        self.unselect_signal.emit()

    def handle_delete(self):
        """
        Handle the deletion of the currently selected racking
        :return: void
        """
        if self.element and hasattr(self.element, 'id'):
            StoreFloor.delete_store_object(object_id=self.element.id)
            self.unselect_signal.emit()


    def new_shelf_creation(self):
        """
        Prepare for the creation of the shelf
        get infos from current racking, creates ElementConstructorData and emit signal to StoreOverview which
        handle the creation of the obejct
        :return:
        """
        constructor = ElementConstructorData(
                    name='',
                    length=self.element.length(),
                    width=self.element.width(),
                    type=SHELF,
                    angle=0,
                    height=0,
                    x_position=0,
                    y_position=0
                )
        self.new_shelf_signal.emit(constructor)

    def display_blank(self):
        """
        Handles the display blank
        :return:
        """
        self.racking_properties.display_blank()
        self.racking_content.display_blank()
        self.racking_properties.disable_all()
        self.racking_content.disable_all()
        self.element = None
        self.racking_properties.element = None
        self.racking_content.element = None



    def create_racking(self):
        """
        Adds element to storeFloor
        Connected to new_element_signal, called when submit button is pressed and element is None
        creates the new storeObject element
        Create StoreObject from ElementConstructorData

        :param constructor:
        :return:
        """
        constructor = self.racking_properties.create_constructor()
        if constructor.type == RACKING:
            # print('creating racking')
            racking = Racking(
                name=constructor.name,
                id=StoreFloor.generate_id(),
                x_position=constructor.x_position,
                y_position=constructor.y_position,
                length=constructor.length,
                width=constructor.width,
                angle=constructor.angle,
                height=constructor.height

            )
            StoreFloor().add_object(racking)
            self.update_child_informations(racking)
            print('rackingInspector element', self.element)
            self.store_viewer.current_drawing = None
            self.store_viewer.repaint()

    def update_child_informations(self, element):
        """
        Update content of properties, content and other child elements of ElementInspector depending oni the type of
        element
        Calls update method on all children sets element
        :param element: StoreObject
        :return:
        """
        # print('update child infos')
        # print(type(element))
        self.racking_properties.enable_all()
        self.element = None
        if element is None:
            # should change for display blank
            self.display_blank()
        elif type(element) is ElementConstructorData:
            print('elementConstructor')
            self.racking_properties.element = None
            self.racking_content.element = None
            self.racking_content.draw_list()
            self.racking_properties.update_informations(element)
            self.racking_content.disable_all()
        elif issubclass(type(element), StoreObject):
            print('element is storeObject')
            self.racking_properties.update_informations(element)
            self.racking_viewer.set_racking(element)
            self.racking_content.update_informations(element)
            self.element = element
