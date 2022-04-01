from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette
from elements.store.storeObject import *
from elements.racking.racking import *
from layout.components.contextInterface.shelfProperties import *
from elements.store.dataClasses import ElementConstructorData

from layout.central.storeOverview.shelfViewerWidget.shelfViewer import ShelfViewer

class RackingContent(QWidget):
    new_shelf_signal = pyqtSignal(ElementConstructorData, name='new_shelf')

    def __init__(self, submit_signal):
        super().__init__()
        self.element = None
        self.main_vbox = QVBoxLayout()
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setBackgroundRole(QPalette.ColorRole.Base)

        self.submit_signal = submit_signal

        self.input_elements = []

        self.list = QListWidget()
        self.main_vbox.addWidget(self.list)
        self.new_shelf_button = QPushButton('+')
        self.new_shelf_button.setDisabled(True)
        self.main_vbox.addWidget(self.new_shelf_button)
        self.new_shelf_button.clicked.connect(self.emit_new_shelf_signal)







        self.setLayout(self.main_vbox)

    def draw_shelf_properties(self):
        pass

    def create_shelf(self):
        print(self.element)
        e = ElementConstructorData(
            name='shelf1',
            type=NONE,
            length=self.element.length(),
            width=self.element.width(),
            height=0,
            x_position=0,
            y_position=0,
            angle=0
        )
        print('creating shelf')

    def emit_new_shelf_signal(self):
        if self.element is not None:
            if type(self.element) == Racking:
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




    def update_informations(self, element: StoreObject):
        self.element = element
        if type(element) is Racking:
            self.new_shelf_button.setDisabled(False)
            print('racking')
        else:
            self.new_shelf_button.setDisabled(True)

    def disable_all(self):
        self.new_shelf_button.setDisabled(True)


