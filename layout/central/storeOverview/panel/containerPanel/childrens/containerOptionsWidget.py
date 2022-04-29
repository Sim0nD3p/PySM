import math

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from layout.central.storeOverview.panel.containerPanel.childrens.customSpinBox import *
from elements.part.Part import *
from elements.ElementLogic.StorageObject import *
from elements.store.dataClasses import *
from backend.PartCatalog import *
from elements.part.Part import *
from dataclasses import dataclass

class ContainerOptionsWidget(QWidget):
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


    container_number_changed = pyqtSignal(int, name='number_container')     # DEPRECIATED

    def __init__(self):
        super().__init__()
        self.storage_object = None      # DEPRECIATED
        self.container_type = None
        self.part_code = None


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
        self.cont_weight_label = QLabel('Masse du contenant: indéterminé')
        self.nb_part_cont_status.setFont(small_font)
        self.nb_part_cont_status.setAlignment(Qt.AlignmentFlag.AlignRight)
        nb_part_grid.addWidget(nb_part_cont_label, 3, 1, 1, 1)
        nb_part_grid.addWidget(self.nb_part_cont_sb, 3, 2, 1, 1)
        nb_part_grid.addWidget(self.nb_part_cont_bt, 3, 3, 1, 1)
        nb_part_grid.addWidget(self.nb_part_cont_status, 4, 1, 1, 3)
        nb_part_grid.addWidget(self.cont_weight_label, 5, 1, 1, 3)

        # nb contenants
        nb_cont_label = QLabel('Nombre contenants')
        self.nb_cont_sb = QSpinBox()
        self.nb_cont_sb.setMaximum(9999)
        self.nb_cont_bt = QPushButton('Auto')
        self.nb_cont_bt.setCheckable(True)
        self.nb_cont_status = QLabel('Nombre de contenants')
        self.nb_cont_status.setFont(small_font)
        self.nb_cont_status.setAlignment(Qt.AlignmentFlag.AlignRight)
        nb_part_grid.addWidget(nb_cont_label, 6, 1, 1, 1)
        nb_part_grid.addWidget(self.nb_cont_sb, 6, 2, 1, 1)
        nb_part_grid.addWidget(self.nb_cont_bt, 6, 3, 1, 1)
        nb_part_grid.addWidget(self.nb_cont_status, 7, 1, 1, 3)

        # DISPOSITION OF CONTAINERS
        self.container_dispo = QComboBox()
        nb_part_grid.addWidget(self.container_dispo, 8, 1, 1, 1)



        self.main_vbox.addLayout(nb_part_grid)

        self.setLayout(self.main_vbox)

        self.buttons_states = [self.nb_part_bt.isChecked(), self.nb_part_cont_bt.isChecked(),
                               self.nb_cont_bt.isChecked()]

        self.nb_part_sb.editingFinished.connect(self.handle_nb_part_exit)
        self.nb_part_cont_sb.editingFinished.connect(self.handle_nb_part_cont_exit)
        self.nb_cont_sb.editingFinished.connect(self.handle_nb_cont_exit)

        self.nb_part_sb.valueChanged.connect(self.handle_nb_part_change)
        self.nb_part_cont_sb.valueChanged.connect(self.handle_nb_part_cont_change)
        self.nb_cont_sb.valueChanged.connect(self.handle_nb_cont_change)

        self.nb_part_bt.clicked.connect(self.handle_nb_part_bt)
        self.nb_part_cont_bt.clicked.connect(self.handle_nb_part_cont_bt)
        self.nb_cont_bt.clicked.connect(self.handle_nb_cont_bt)

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
        print(value)
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
        Handles click on nb_part_cont_bt
        Calculates the maximum number of parts in a container according to the weight of the part and the weight
        capacity of the container
        :return:
        """
        if self.part_code and PartCatalog.get_part(self.part_code):
            part = PartCatalog.get_part(self.part_code)
            print(self.container_type.weight_capacity)
            if part.weight() and self.container_type.weight_capacity:
                qte = math.floor(self.container_type.weight_capacity / part.weight())
                self.nb_part_cont = qte
                self.update_ui()



    def handle_nb_part_cont_change(self, value):
        """
        Handle changes nb_part_cont_change
        :return:
        """
        self.nb_part_cont = value
        if self.nb_part_cont != 0:
            print('calc nb_cont')
            if self.part_code and self.container_type:
                if PartCatalog.get_part(self.part_code) and\
                        PartCatalog.get_part(self.part_code).weight():
                    self.cont_weight_label.setText('Masse de contenant: ' + str(PartCatalog.get_part(
                        self.part_code).weight() * self.nb_part_cont))
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

    def handle_nb_cont_bt(self):
        """
        Handles button nb_cont
        :return:
        """
        pass

    def handle_nb_cont_change(self, value):
        self.nb_cont = value
        # Other values updated on exitEditing because it would cause loop

        self.update_ui()


    def handle_nb_cont_exit(self):
        """
        Handles changes in nb_cont spinBox,
        calculate the number of part per containers according to the number of container set
        if the number of part in container is too high (according to weight), we change the number of part
        TODO will need to change behavior so that its more logic, when nb_part = 0 and we change nb_cont, bug
        :return:
        """
        self.nb_cont = self.nb_cont_sb.value()
        if self.nb_part_cont != 0 and self.nb_cont != math.ceil(self.nb_part / self.nb_part_cont):
            print('calc elements')
            self.nb_part_cont = math.ceil(self.nb_part / self.nb_cont)
            part = PartCatalog.get_part(self.part_code)
            if part and part.weight() and \
                    self.nb_part_cont * part.weight() > self.container_type.weight_capacity:
                self.nb_part_cont = math.floor(self.container_type.weight_capacity / part.weight())
                self.nb_part = math.floor(self.nb_part_cont * self.nb_cont)

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

    def get_options_data(self):
        return ContainerOptions(
            nb_cont=self.nb_cont,
            nb_part=self.nb_part,
            stacked=0       # TODO ADD STACK FIELD IN WIDGET OPTIONS
        )


    def display_blank(self):
        """
        Display blank values for all input elements
        :return:
        """
        self.storage_object = None
        self.container_type = None
        self.part_code = None
        self.nb_part = 0
        self.nb_cont = 0
        self.nb_part_cont = 0
        self.update_ui()

    def display_content(self, content: StorageObject):
        self.storage_object = content   # DEPRECIATED
        self.container_type = content.container_type()
        self.part_code = content.part_code
        self.nb_cont = content.container_number()
        self.nb_part = content.storage_capacity()
        if self.nb_cont != 0:
            self.nb_part_cont = math.ceil(self.nb_part / self.nb_cont)
        self.update_ui()


    def update_information_old(self, element: StorageObject):
        print('ContainerOptions: received element to update widget')
        if issubclass(type(element), StorageObject):
            self.storage_object = element
            self.nb_cont = self.storage_object.container_number()
            self.nb_part_cont = self.storage_object.storage_capacity()
            self.update_ui()
        else:
            self.storage_object = None
        # print('info updated on containerOption')

