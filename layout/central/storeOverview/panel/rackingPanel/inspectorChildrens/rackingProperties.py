from PyQt6.QtGui import QFont
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt
from elements.store.dataClasses import *
from elements.elementsTypes import *
from elements.store.storeObject import StoreObject
from layout.settings.settings import Settings
from PyQt6.QtCore import *
from elements.ElementLogic.dataClasses import *

class RackingProperties(QWidget):
    geometry_change_signal = pyqtSignal(Geometry, name='geometry_change')

    def __init__(self, submit_signal, new_element_signal):
        super().__init__()
        self.element = None
        self.submit_signal = submit_signal
        self.new_element_signal = new_element_signal
        self.main_vbox = QVBoxLayout()
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.input_elements = []

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
        self.input_elements.append(self.name_le)
        self.name_le.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(self.name_label)
        name_hbox.addWidget(self.name_le)
        self.main_vbox.addLayout(name_hbox)

        # ID
        id_hbox = QHBoxLayout()
        id_label = QLabel('ID: ')
        self.id_label = QLabel('id')
        id_font = QFont('Arial')
        id_font.setWeight(500)
        self.id_label.setFont(id_font)
        id_hbox.addWidget(id_label)
        id_hbox.addWidget(self.id_label)
        self.main_vbox.addLayout(id_hbox)

        # TYPE
        type_hbox = QHBoxLayout()
        self.type_cb = QComboBox()
        self.input_elements.append(self.type_cb)
        self.type_cb.setPlaceholderText('type')
        self.draw_types_cb()
        type_label = QLabel('Type')
        type_hbox.addWidget(type_label)
        type_hbox.addWidget(self.type_cb)
        self.main_vbox.addLayout(type_hbox)

        # GEOMETRY
        geo_grid = QGridLayout()

        self.x_pos_sb = QSpinBox()
        self.x_pos_sb.valueChanged.connect(self.handle_geometry_change)
        self.input_elements.append(self.x_pos_sb)
        self.x_pos_sb.setMaximum(9999)
        self.x_pos_sb.setMinimum(-9999)
        x_pos_label = QLabel('Position x')
        self.y_pos_sb = QSpinBox()
        self.input_elements.append(self.y_pos_sb)
        self.y_pos_sb.valueChanged.connect(self.handle_geometry_change)
        self.y_pos_sb.setMaximum(9999)
        self.y_pos_sb.setMinimum(-9999)
        y_pos_label = QLabel('Position y')

        geo_grid.addWidget(x_pos_label, 0, 0, 1, 1)
        geo_grid.addWidget(self.x_pos_sb, 0, 1, 1, 1)
        geo_grid.addWidget(y_pos_label, 1, 0, 1, 1)
        geo_grid.addWidget(self.y_pos_sb, 1, 1, 1, 1)

        # DIMENSIONS
        len_label = QLabel('Longueur')
        self.len_sb = QSpinBox()
        self.len_sb.valueChanged.connect(self.handle_geometry_change)
        self.len_sb.setMaximumWidth(50)
        self.input_elements.append(self.len_sb)
        self.len_sb.setMaximum(9999)
        wid_label = QLabel('Largeur')
        self.wid_sb = QSpinBox()
        self.wid_sb.valueChanged.connect(self.handle_geometry_change)
        self.input_elements.append(self.wid_sb)
        self.wid_sb.setMaximum(9999)

        geo_grid.addWidget(len_label, 2, 0, 1, 1)
        geo_grid.addWidget(self.len_sb, 2, 1, 1, 1)
        geo_grid.addWidget(wid_label, 3, 0, 1, 1)
        geo_grid.addWidget(self.wid_sb, 3, 1, 1, 1)

        # ANGLE | HEIGHT

        self.ang_sb = QSpinBox()
        self.ang_sb.valueChanged.connect(self.handle_geometry_change)
        self.input_elements.append(self.ang_sb)
        self.ang_sb.setMinimum(0)
        self.ang_sb.setMaximum(360)
        ang_label = QLabel('Angle')
        self.hei_sb = QSpinBox()
        self.hei_sb.valueChanged.connect(self.handle_geometry_change)
        self.input_elements.append(self.hei_sb)
        self.hei_sb.setMaximum(Settings().store_object_max_height)
        hei_label = QLabel('Hauteur')


        geo_grid.addWidget(ang_label, 4, 0, 1, 1)
        geo_grid.addWidget(self.ang_sb, 4, 1, 1, 1)
        geo_grid.addWidget(hei_label, 5, 0, 1, 1)
        geo_grid.addWidget(self.hei_sb, 5, 1, 1, 1)


        self.main_vbox.addLayout(geo_grid)

        # SUBMIT BUTTON
        # self.sub_button = QPushButton('Ok')
        # self.sub_button.clicked.connect(self.send_submit_signal)
        # self.main_vbox.addWidget(self.sub_button)

        self.create_layout()

    def handle_geometry_change(self):
        """
        Triggered on change of any geometry and emit geometry_change_signal which is received by rackingInspector
        :return:
        """
        print('handling geometry change in rackingProperties')
        height = self.hei_sb.value()
        width = self.wid_sb.value()
        length = self.len_sb.value()
        x_pos = self.x_pos_sb.value()
        y_pos = self.y_pos_sb.value()
        angle = self.ang_sb.value()
        geo = Geometry(length=length, width=width, height=height, x_position=x_pos, y_position=y_pos, angle=angle,
                       name='')

        self.geometry_change_signal.emit(geo)


    def create_constructor(self):
        """
        Creates constructor to create racking from values in properties form
        :return:
        """
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
        return constructor


    def send_submit_signal_old(self):
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
            self.modify_store_object()

            self.submit_signal.emit('repaint submit')

    def modify_store_object(self):
        """
        Modify the given StoreObject with the values in widget
        :param element: StoreObject
        :return: void
        """
        print('modify store')
        if self.element:
            self.element.name = self.name_le.text()
            self.element.set_x_position(self.x_pos_sb.value())
            self.element.set_y_position(self.y_pos_sb.value())
            self.element.set_length(self.len_sb.value())
            self.element.set_width(self.wid_sb.value())
            self.element.set_angle(self.ang_sb.value())
            self.element.set_height(self.hei_sb.value())



    def update_informations(self, element):
        """
        Element is either ElementConstructorData or storeObject,
        updates informations in widget
        :param element:
        :return:
        """
        # type existant or new
        if type(element) is ElementConstructorData:
            self.element = None
            self.display_from_constructor(element)
        elif issubclass(type(element), StoreObject):
            self.element = element
            self.display_from_object(element)

    def display_from_constructor(self, constructor: ElementConstructorData):
        """
        Displays values of new drawing in widget
        :param constructor: ElementConstructorData
        :return: void
        """
        self.name_le.setText(constructor.name)
        self.id_label.setText('Non attribué')
        self.len_sb.setValue(constructor.length)
        self.wid_sb.setValue(constructor.width)
        self.x_pos_sb.setValue(constructor.x_position)
        self.y_pos_sb.setValue(constructor.y_position)
        self.ang_sb.setValue(constructor.angle)
        self.enable_all()

    def display_from_object(self, store_object: StoreObject):
        """
        Displays values of properties of object in widget
        :param store_object: StoreObject
        :return:
        """
        self.name_le.setText(store_object.name)
        self.id_label.setText('#' + str(store_object.id))
        self.len_sb.setValue(store_object.length())
        self.wid_sb.setValue(store_object.width())
        self.x_pos_sb.setValue(store_object.x_position())
        self.y_pos_sb.setValue(store_object.y_position())
        self.ang_sb.setValue(store_object.angle())
        self.hei_sb.setValue(store_object.height())
        self.type_cb.setCurrentIndex(self.type_cb.findData(store_object.type))
        self.enable_all()

    def display_blank(self):
        """
        Resets all values of input widgets and disables the input widgets
        :return: void
        """
        self.name_le.setText('')
        self.id_label.setText('#######')
        self.len_sb.setValue(0)
        self.wid_sb.setValue(0)
        self.x_pos_sb.setValue(0)
        self.y_pos_sb.setValue(0)
        self.ang_sb.setValue(0)
        self.hei_sb.setValue(0)
        self.disable_all()


    def disable_all(self):
        for element in self.input_elements:
            element.setDisabled(True)

    def enable_all(self):
        for element in self.input_elements:
            element.setDisabled(False)





    def draw_types_cb(self):
        self.type_cb.addItem('Racking', userData=RACKING)
        self.type_cb.addItem('Autre', userData=OTHER)

    def create_layout(self):
        self.setLayout(self.main_vbox)
