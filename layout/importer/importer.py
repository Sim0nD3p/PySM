from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QStackedLayout, \
    QComboBox, QFileDialog
import json
from layout.importer.treePropertiesEditor import TreePropretiesEditor
from layout.importer.xmlImporter import XmlImporter
from layout.importer.jsonImporter import JsonImporter
from layout.importer.confirmationWidget import ConfirmationWidget


class ImporterWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.importer = Importer(parent)

    def open_window(self, window):
        window.setCentralWidget(self.importer)
        window.setGeometry(200, 100, 900, 500)
        window.setWindowTitle('Importer catalogue')


class typeSelection(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.selected_type = None
        self.typeOptions = ['fichier csv', 'fichier json', 'fichier xml']
        self.file_types = ['csv', 'json', 'xml']
        self.create_layout()

    def make_entry_line(self, element1, element2):
        widget = QWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(element1)
        hbox.addWidget(element2)
        widget.setLayout(hbox)
        return widget

    def file_dir(self):
        default_directory = 'C:/Users/simon/Desktop'
        print('should display file dialog')
        fd = QFileDialog(directory=default_directory)
        fn = fd.getOpenFileName()
        file_name = fn[0]
        file_type = file_name.split('.')[len(file_name.split('.')) - 1]
        if file_type == self.selected_type:
            print('we good')
            self.parent.update_import_window(file_name, file_type)
        else:
            print('error')

    def set_file_type(self, ft_index):
        self.selected_type = self.file_types[ft_index]
        self.parent.change_import_window(self.selected_type)

    def create_layout(self):
        vbox = QVBoxLayout()

        type_selector = QComboBox()
        type_selector.currentIndexChanged.connect(self.set_file_type)
        type_selector.addItems(self.typeOptions)
        type = QLabel('Type')
        line1 = self.make_entry_line(type, type_selector)

        select_file = QLabel('Fichier')
        file_selector = QPushButton('Explorateur de fichiers')
        file_selector.clicked.connect(self.file_dir)
        line2 = self.make_entry_line(select_file, file_selector)

        vbox.addWidget(line1)
        vbox.addWidget(line2)
        self.setLayout(vbox)




'''
@classmethod
- can change class variables for all instances
- global method that will apply to all instances 

alternate constructor

class Employee(name, surname, salary)

new_emp = Employee('John', 'Smith', 50000)
new_emp = Employee.from_string('john-smith-50000')

def from_string(cls, input_data):
    'handling data'
    return cls(name, surname, salary)
    


'''






class Importer(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.types = ['csv', 'json', 'xml']
        self.parent = parent
        self.csv_importer = QLabel('csv')
        self.json_importer = JsonImporter(parent=self)
        self.xml_importer = XmlImporter(parent=self)

        self.main_stacked_layout = QStackedLayout()

        self.confirmation_widget = ConfirmationWidget(parent=self)
        self.selection_widget = QWidget()

        self.stacked_panel = QWidget()
        self.panel_layout = QStackedLayout()
        self.panel_layout.addWidget(self.csv_importer)
        self.panel_layout.addWidget(self.json_importer)
        self.panel_layout.addWidget(self.xml_importer)
        self.stacked_panel.setLayout(self.panel_layout)

        self.selection = typeSelection(parent=self)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.selection)
        self.hbox.addWidget(self.stacked_panel)
        self.selection_widget.setLayout(self.hbox)

        self.main_stacked_layout.addWidget(self.selection_widget)
        self.main_stacked_layout.addWidget(self.confirmation_widget)

        self.setLayout(self.main_stacked_layout)

    def change_import_window(self, type):
        # print('change import window')
        index = self.types.index(type)
        self.panel_layout.setCurrentIndex(index)

    def update_import_window(self, file_name, file_type):
        # print('update import window')
        if file_type == 'json':
            self.json_importer.update_tree(file_name)

    def main_update(self):
        """
        calls the main.py file to update UI
        :param list:
        :return:
        """
        # print(list)
        self.main_stacked_layout.setCurrentIndex(0)
        self.parent.part_catalog_update()

    def confirm_import(self, list):
        # print('confirming import list')
        self.main_stacked_layout.setCurrentIndex(1)
        self.confirmation_widget.display_import_list(list)



