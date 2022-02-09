import os
from layout.importer.catalogInputModules.historyFormatterScripts.parserFromPFEP import parseFromPFEP
from backend.PartCatalog import PartCatalog


from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFileDialog, QPushButton
from os import listdir

class HistoryImporter(QWidget):
    def __init__(self):
        super().__init__()

        self.main_vbox = QVBoxLayout()
        self.dropdown = QComboBox()

        self.fd = QFileDialog()
        self.fd.fileSelected.connect(self.handle_file_change)
        self.selected_source_file = ''
        self.current_selected_file_label = QLabel('')
        self.submit_button = QPushButton('Suivant')

        self.file_button = QPushButton('Sélectionner fichier')
        self.file_button.clicked.connect(self.show_file_dialog)
        self.draw_file_selector()
        self.draw_parser_selector()
        self.draw()

    def draw_parser_selector(self):
        """
        Selection for the order data formatter
        :return:
        """
        hbox = QHBoxLayout()
        label = QLabel('Extracteur de données: ')
        list = os.listdir('C:/Users/simon/Documents/Techno-Fab/PySM/PySM/layout/importer/catalogInputModules/historyFormatterScripts')

        for el in list:
            if el != '__pycache__':
                self.dropdown.addItem(el)

        hbox.addWidget(label)
        hbox.addWidget(self.dropdown)

        self.main_vbox.addLayout(hbox)

    def draw_file_selector(self):
        """
        Draws the file selector row
        :return:
        """
        hbox = QHBoxLayout()
        label = QLabel('Fichier source:')
        hbox.addWidget(label)
        hbox.addWidget(self.current_selected_file_label)
        hbox.addWidget(self.file_button)
        self.main_vbox.addLayout(hbox)

    def show_file_dialog(self):
        """
        Shows the file dialog
        :return:
        """
        directory = 'C:/Users/simon/Documents/Techno-Fab/PySM sample dir'
        self.fd.setDirectory(directory)
        self.selected_source_file = self.fd.getOpenFileName()


        print(self.fd.directory().absolutePath())
        self.current_selected_file_label.setText(self.selected_source_file[0])


    def handle_file_change(self):
        directory = self.fd.directory()
        print(directory)

    def get_order_part(self, order):
        if order.part_code is not None:
            if PartCatalog.check_presence(order.part_code):
                part = PartCatalog.get_part(order.part_code)
                return part
            else:
                return 'error - part not present'
        else:
            return 'error - no part_code in order'

    def add_orders_to_catalog(self, pool):
        for order in pool:
            part = self.get_order_part(order)
            part.add_order_to_history(order)


    def make_order_pool(self):
        """
        Creates order pool with all the orders found in targeted file
        :return: order pool
        """
        print('make order pool')
        parser_name = self.dropdown.itemText(self.dropdown.currentIndex())
        if parser_name == 'parserFromPFEP.py':
            print('using parserFromPFEP.py')
            print(self.selected_source_file[0])
            pool = parseFromPFEP(self.selected_source_file[0])

        if len(pool):
            self.add_orders_to_catalog(pool)



    def draw(self):
        self.main_vbox.setContentsMargins(100, 50, 100, 250)
        self.main_vbox.addWidget(self.submit_button)
        self.setLayout(self.main_vbox)

    