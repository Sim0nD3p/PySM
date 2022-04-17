import math

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.central.storeOverview.panel.containerPanel.childrens.customSpinBox import *
from elements.part.Part import *
from elements.ElementLogic.StorageObject import *
from backend.PartCatalog import *
from elements.part.Part import *

class ContainerOptions(QWidget):
    """
    We want to know how many container we need
        if we have place, checkbox to stack containers
    """
    nb_cont_manual_message = 'Nombre de contenants entré manuellement'
    nb_part_manual_message = 'Nombre de pièces entré manuellement'
    nb_part_cont_manual_message = 'Nombre de pièces par contenant entré manuellement'

    nb_cont_auto_message = 'Nombre de contenants calculé'
    nb_part_auto_message = 'Nombre de pièces calculé'
    nb_part_cont_auto_message = 'Nombre de pièces par contenant calculé'


    container_number_changed = pyqtSignal(int, name='number_container')

    def __init__(self):
        super().__init__()
        self.storage_object = None

        self.setMaximumWidth(300)
        self.main_vbox = QVBoxLayout()
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        title = QLabel('Options de contenant')
        self.main_vbox.addWidget(title)

        self.nb_part = 0
        self.nb_part_cont = 0
        self.nb_cont = 0

        small_font = QFont('Arial')
        small_font.setPointSize(8)
        small_font.setWeight(400)

        nb_part_grid = QGridLayout()

        # nb pieces
        nb_part_label = QLabel('Nombre de pièces à stocker')
        self.nb_part_sb = QSpinBox()
        self.nb_part_sb.setMaximum(9999)
        self.nb_part_bt = QPushButton('Auto')
        self.nb_part_bt.setCheckable(True)
        self.nb_part_status = QLabel('Nombre de pièce calculé automatiquement')
        self.nb_part_status.setFont(small_font)
        self.nb_part_status.setAlignment(Qt.AlignmentFlag.AlignRight)
        nb_part_grid.addWidget(nb_part_label, 1, 1, 1, 1)
        nb_part_grid.addWidget(self.nb_part_sb, 1, 2, 1, 1)
        nb_part_grid.addWidget(self.nb_part_bt, 1, 3, 1, 1)
        nb_part_grid.addWidget(self.nb_part_status, 2, 1, 1, 3)

        # nb pieces par contenants
        nb_part_cont_label = QLabel('Pièce / contenant')
        self.nb_part_cont_sb = QSpinBox()
        self.nb_part_cont_sb.setMaximum(9999)
        self.nb_part_cont_bt = QPushButton('Maximiser masse')
        self.nb_part_cont_bt.setCheckable(True)
        self.nb_part_cont_status = QLabel('Nombre de pièces limité par masse')
        self.nb_part_cont_status.setFont(small_font)
        self.nb_part_cont_status.setAlignment(Qt.AlignmentFlag.AlignRight)
        nb_part_grid.addWidget(nb_part_cont_label, 3, 1, 1, 1)
        nb_part_grid.addWidget(self.nb_part_cont_sb, 3, 2, 1, 1)
        nb_part_grid.addWidget(self.nb_part_cont_bt, 3, 3, 1, 1)
        nb_part_grid.addWidget(self.nb_part_cont_status, 4, 1, 1, 3)

        # nb contenants
        nb_cont_label = QLabel('Nombre contenants')
        self.nb_cont_sb = QSpinBox()
        self.nb_cont_sb.setMaximum(9999)
        self.nb_cont_bt = QPushButton('Auto')
        self.nb_cont_bt.setCheckable(True)
        self.nb_cont_status = QLabel('Nombre de contenants')
        self.nb_cont_status.setFont(small_font)
        self.nb_cont_status.setAlignment(Qt.AlignmentFlag.AlignRight)
        nb_part_grid.addWidget(nb_cont_label, 5, 1, 1, 1)
        nb_part_grid.addWidget(self.nb_cont_sb, 5, 2, 1, 1)
        nb_part_grid.addWidget(self.nb_cont_bt, 5, 3, 1, 1)
        nb_part_grid.addWidget(self.nb_cont_status, 6, 1, 1, 3)


        self.main_vbox.addLayout(nb_part_grid)

        self.setLayout(self.main_vbox)

        self.buttons_states = [self.nb_part_bt.isChecked(), self.nb_part_cont_bt.isChecked(),
                               self.nb_cont_bt.isChecked()]

        self.nb_part_sb.editingFinished.connect(self.handle_nb_part_exit)
        self.nb_part_cont_sb.editingFinished.connect(self.handle_nb_part_cont_exit)
        self.nb_cont_sb.editingFinished.connect(self.handle_nb_cont_exit)

        self.nb_part_sb.valueChanged.connect(self.handle_nb_part_change)
        self.nb_part_cont_sb.valueChanged.connect(self.handle_nb_part_cont_change)

        self.nb_part_bt.clicked.connect(self.handle_nb_part_bt)
        self.nb_part_cont_bt.clicked.connect(self.handle_nb_part_cont_bt)

    def test(self):
        print('editing finished')

    def handle_nb_part_bt(self):
        """
        Handles when the button nb_part_bt is clicked, sets the maximum number for part inventory to a certain formula tbd
        # TODO FORMULA SAFETY STOCK
        :return:
        """
        print(self.buttons_states[0])
        calculated_value = 50
        if not self.buttons_states[0]:
            print('should change')
            self.nb_part = calculated_value
        else:
            self.nb_part = 0
        self.update_ui()

    def handle_nb_part_change(self, value):
        self.nb_part = value
        if self.nb_part_cont != 0:
            print('calc nb_cont')
            self.nb_cont = math.ceil(self.nb_part / self.nb_part_cont)


        self.update_ui()

    def handle_nb_part_exit(self):
        """
        Handles changes in nb_Part spinBox
        :return:
        """
        self.nb_part_bt.setChecked(False)


        self.nb_part_status.setText(self.nb_part_manual_message)
        self.nb_part_cont_status.setText(self.nb_part_cont_manual_message)
        self.nb_cont_status.setText(self.nb_cont_auto_message)

        self.update_ui()


    def handle_nb_part_cont_bt(self):
        """
        When the nb_part_cont_bt button is clicked, the number of part per container is set in regards to maximum weigth

        :return:
        """
        if type(self.storage_object) == StorageObject:
            if self.storage_object.part_code:
                part = PartCatalog.get_part(self.storage_object.part_code)
                if part.specifications.weight:
                    part_capacity = self.storage_object.container_type().weight_capacity / part.specifications.weight
                    self.nb_part_cont = part_capacity
                    self.update_ui()

                else:
                    print('part has no weight')
            else:
                print('no part selected')

    def handle_nb_part_cont_change(self, value):
        """
        Handle changes nb_part_cont_change
        :return:
        """
        self.nb_part_cont = value
        if self.nb_part_cont != 0:
            print('calc nb_cont')
            self.nb_cont = math.ceil(self.nb_part / self.nb_part_cont)

        self.update_ui()


    def handle_nb_part_cont_exit(self):
        """
        Handles changes in nb_part_cont spinBox
        :return:
        """


        self.nb_part_status.setText(self.nb_part_manual_message)
        self.nb_part_cont_status.setText(self.nb_part_cont_manual_message)
        self.nb_cont_status.setText(self.nb_cont_auto_message)

        self.update_ui()

    def handle_nb_cont_changed(self, value):
        self.nb_cont = value
        # TODO update other values
        self.container_number_changed.emit(self.nb_cont)


    def handle_nb_cont_exit(self):
        """
        Handles changes in nb_cont spinBox
        :return:
        """
        self.nb_cont = self.nb_cont_sb.value()

        self.nb_part_status.setText(self.nb_part_auto_message)
        self.nb_part_cont_status.setText(self.nb_part_cont_auto_message)
        self.nb_cont_status.setText(self.nb_cont_manual_message)

        self.update_ui()


    def update_ui(self):
        """
        Updates the UI values
        :return:
        """
        # print('part', self.nb_part, 'part_cont', self.nb_part_cont, 'cont', self.nb_cont)
        self.nb_part_sb.setValue(self.nb_part)
        self.nb_part_cont_sb.setValue(self.nb_part_cont)
        self.nb_cont_sb.setValue(self.nb_cont)

        # print(self.buttons_states[0])


    def handle_auto_nb_part(self):
        pass

    def update_information(self, element):
        print('ContainerOptions: received element to update widget')
        if type(element) == StorageObject:
            self.storage_object = element
        else:
            self.storage_object = None
        # print('info updated on containerOption')


