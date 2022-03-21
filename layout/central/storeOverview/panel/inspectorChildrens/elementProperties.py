from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QSpinBox
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt
from elements.store.dataClasses import *
from elements.elementsTypes import *
from elements.store.storeObject import StoreObject
from layout.settings.settings import Settings


class ElementProperties(QWidget):
    def __init__(self, submit_signal, new_element_signal):
        super().__init__()
        self.element = None
        self.submit_signal = submit_signal
        self.new_element_signal = new_element_signal
        self.main_vbox = QVBoxLayout()
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setBackgroundRole(QPalette.ColorRole.Base)

        # TITLE
        title = QLabel('Propriétés')
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        title.setMaximumHeight(25)
        self.main_vbox.addWidget(title)

        # NAME
        self.name_label = QLabel('Nom')
        self.name_le = QLineEdit()
        self.name_le.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(self.name_label)
        name_hbox.addWidget(self.name_le)
        self.main_vbox.addLayout(name_hbox)

        # TYPE
        type_hbox = QHBoxLayout()
        self.type_cb = QComboBox()
        self.type_cb.setPlaceholderText('type')
        self.draw_types_cb()
        type_label = QLabel('Type')
        type_hbox.addWidget(type_label)
        type_hbox.addWidget(self.type_cb)
        self.main_vbox.addLayout(type_hbox)

        # POSITION
        pos_hbox = QHBoxLayout()
        self.x_pos_sb = QSpinBox()
        self.x_pos_sb.setMaximum(9999)
        self.x_pos_sb.setMinimum(-9999)
        x_pos_label = QLabel('Position x')
        self.y_pos_sb = QSpinBox()
        self.y_pos_sb.setMaximum(9999)
        self.y_pos_sb.setMinimum(-9999)
        y_pos_label = QLabel('Position y')
        pos_hbox.addWidget(x_pos_label)
        pos_hbox.addWidget(self.x_pos_sb)
        pos_hbox.addWidget(y_pos_label)
        pos_hbox.addWidget(self.y_pos_sb)
        self.main_vbox.addLayout(pos_hbox)

        # DIMENSIONS
        dim_hbox = QHBoxLayout()
        len_label = QLabel('Longueur')
        self.len_sb = QSpinBox()
        self.len_sb.setMaximum(9999)
        wid_label = QLabel('Largeur')
        self.wid_sb = QSpinBox()
        self.wid_sb.setMaximum(9999)
        dim_hbox.addWidget(len_label)
        dim_hbox.addWidget(self.len_sb)
        dim_hbox.addWidget(wid_label)
        dim_hbox.addWidget(self.wid_sb)
        self.main_vbox.addLayout(dim_hbox)

        # ANGLE | HEIGHT
        ah_hbox = QHBoxLayout()
        self.ang_sb = QSpinBox()
        self.ang_sb.setMinimum(0)
        self.ang_sb.setMaximum(360)
        ang_label = QLabel('Angle')
        self.hei_sb = QSpinBox()
        self.hei_sb.setMaximum(Settings().store_object_max_height)
        hei_label = QLabel('Hauteur')
        ah_hbox.addWidget(ang_label)
        ah_hbox.addWidget(self.ang_sb)
        ah_hbox.addWidget(hei_label)
        ah_hbox.addWidget(self.hei_sb)
        self.main_vbox.addLayout(ah_hbox)

        # SUBMIT BUTTON
        self.sub_button = QPushButton('Ok')
        self.sub_button.clicked.connect(self.send_submit_signal)
        self.main_vbox.addWidget(self.sub_button)

        self.create_layout()

    def send_submit_signal(self):
        """"
        when creating and modifying elements
        Sends submit signal to main inspector widget
        Gets data from widget and sends it to ElementInspector if new element (self.element = None)
        """
        index = self.type_cb.currentIndex()
        if self.element is None:
            constructor = ElementConstructorData(
                x_position=self.x_pos_sb.value(),
                y_position=self.y_pos_sb.value(),
                length=self.len_sb.value(),
                width=self.wid_sb.value(),
                angle=self.ang_sb.value(),
                height=self.hei_sb.value(),
                type=self.type_cb.itemData(self.type_cb.currentIndex()),
                name=self.name_le.text()
            )
            self.new_element_signal.emit(constructor)
            # new element, create constructor
        else:
            self.modify_store_object(self.element)

            self.submit_signal.emit('repaint submit')

    def modify_store_object(self, element: StoreObject):
        """
        Modify the given StoreObject with the values in widget
        :param element: StoreObject
        :return: void
        """
        element.name = self.name_le.text()
        element.set_x_position(self.x_pos_sb.value())
        element.set_y_position(self.y_pos_sb.value())
        element.set_length(self.len_sb.value())
        element.set_width(self.wid_sb.value())
        element.set_angle(self.ang_sb.value())
        element.set_height(self.hei_sb.value())



    def update_informations(self, element):
        """
        Element is either ElementConstructorData or storeObject,
        updates informations in widget
        :param element:
        :return:
        """
        # type existant or new
        if type(element) is ElementConstructorData:
            self.display_from_constructor(element)
        elif issubclass(type(element), StoreObject):
            self.element = element
            # print(element)
            self.display_from_object(element)
            # self.name_label.setText()

    def display_from_constructor(self, constructor: ElementConstructorData):
        """
        Displays values of new drawing in widget
        :param constructor: ElementConstructorData
        :return: void
        """
        self.name_le.setText(constructor.name)
        self.len_sb.setValue(constructor.length)
        self.wid_sb.setValue(constructor.width)
        self.x_pos_sb.setValue(constructor.x_position)
        self.y_pos_sb.setValue(constructor.y_position)
        self.ang_sb.setValue(constructor.angle)

    def display_from_object(self, store_object: StoreObject):
        """
        Displays values of properties of object in widget
        :param store_object: StoreObject
        :return:
        """
        self.name_le.setText(store_object.name)
        self.len_sb.setValue(store_object.length())
        self.wid_sb.setValue(store_object.width())
        self.x_pos_sb.setValue(store_object.x_position())
        self.y_pos_sb.setValue(store_object.y_position())
        self.ang_sb.setValue(store_object.angle())
        self.hei_sb.setValue(store_object.height())



    def draw_types_cb(self):
        self.type_cb.addItem('Racking', userData=RACKING)

    def create_layout(self):
        self.setLayout(self.main_vbox)
