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

class RackingInspector(QTabWidget):
    """
    Interface between racking and backend (racking in StoreFloor), to manage racking by user
    TODO: change submit signal to buttons in RackingInspector directly
    """
    submit_signal = pyqtSignal(str) # changed for new_element
    new_element_signal = pyqtSignal(ElementConstructorData)     # create new element
    def __init__(self, store_viewer: StoreTopVisualizer):
        super().__init__()
        self.store_viewer = store_viewer
        self.racking_properties = RackingProperties(submit_signal=self.submit_signal,
                                                    new_element_signal=self.new_element_signal)
        self.addTab(self.racking_properties, 'Informations générales')

        self.racking_content = RackingContent(submit_signal=self.submit_signal)


        self.addTab(self.racking_content, 'Contenu')
        self.current_element = None
        self.submit_signal.connect(self.handle_submit)
        self.new_element_signal.connect(self.create_element)

    def create_element(self, constructor: ElementConstructorData):
        """
        Adds element to storeFloor
        Connected to new_element_signal, called when submit button is pressed and element is None
        creates the new storeObject element
        Create StoreObject from ElementConstructorData

        :param constructor:
        :return:
        """
        if constructor.type == RACKING:
            # print('creating racking')
            racking = Racking(
                name=constructor.name,
                id=1010,
                x_position=constructor.x_position,
                y_position=constructor.y_position,
                length=constructor.length,
                width=constructor.width,
                angle=constructor.angle,
                height=constructor.height

            )
            StoreFloor().add_object(racking)
            self.update_child_informations(racking)
            self.store_viewer.current_drawing = None
            self.store_viewer.repaint()


    def handle_submit(self, e):
        print('hanlde submit in elementInspector')
        self.store_viewer.paintGL()
        self.store_viewer.repaint()



    def update_child_informations(self, element):
        """
        Update content of properties, content and other child elements of ElementInspector
        :param element: StoreObject
        :return:
        """
        print('update child infos')
        self.racking_properties.enable_all()
        if element is None:
            self.racking_properties.display_blank()
            self.racking_properties.element = None
            self.racking_properties.disable_all()
            self.racking_content.disable_all()
        elif type(element) is ElementConstructorData:
            self.racking_properties.element = None
            self.racking_properties.update_informations(element)
        elif issubclass(type(element), StoreObject):
            # print('element is storeObject')
            self.current_element = element
            self.racking_properties.update_informations(element)
            self.racking_content.update_informations(element)
