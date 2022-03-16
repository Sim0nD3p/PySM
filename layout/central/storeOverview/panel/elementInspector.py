from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QTabWidget, QComboBox, QSpinBox
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt, pyqtSignal
from layout.central.storeOverview.panel.inspectorChildrens.elementProperties import ElementProperties


class ElementInspector(QTabWidget):
    submit_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.element_properties = ElementProperties(submit_signal=self.submit_signal)
        self.addTab(self.element_properties, 'Informations générales')
        self.submit_signal.connect(self.create_element)

    def create_element(self, e):
        print('create element')
        print(e)



    def update_child_informations(self, element):
        """
        Update content of properties, content and other child elements of ElementInspector
        :param element: StoreObject
        :return:
        """

        self.element_properties.update_informations(element)