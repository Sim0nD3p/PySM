from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QTabWidget, QComboBox, QSpinBox
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt, pyqtSignal
from layout.central.storeOverview.panel.inspectorChildrens.elementProperties import ElementProperties
from layout.central.storeOverview.physicalViewer.storeOverallTopView import StoreTopVisualizer
from elements.store.dataClasses import *
from elements.elementsTypes import *
from elements.store.storeObject import StoreObject
from elements.racking.racking import Racking
from backend.storeFloor import StoreFloor

class ElementInspector(QTabWidget):
    """
    Interact with StoreFloor
    """
    submit_signal = pyqtSignal(str) # changed for new_element
    new_element_signal = pyqtSignal(ElementConstructorData)     # create new element
    def __init__(self, store_viewer: StoreTopVisualizer):
        super().__init__()
        self.store_viewer = store_viewer
        self.element_properties = ElementProperties(submit_signal=self.submit_signal,
                                                    new_element_signal=self.new_element_signal)
        self.addTab(self.element_properties, 'Informations générales')
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
        if type(element) is ElementConstructorData:
            self.element_properties.element = None
            self.element_properties.update_informations(element)
        elif issubclass(type(element), StoreObject):
            # print('element is storeObject')
            self.current_element = element
            self.element_properties.update_informations(element)