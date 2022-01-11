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




class JsonImporter_old(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.tree = TreePropretiesEditor()
        self.create_layout()

    def create_layout(self):
        vbox = QVBoxLayout()

        button = QPushButton('button')
        button.clicked.connect(self.get_xml)
        vbox.addWidget(self.tree)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def get_xml(self):
        self.tree.submit_template()


    def update_tree(self, file_name):
        print('update treeeee')
        self.setStyleSheet('background-color:red')
        self.json_parser(file_name)

    def json_parser(self, file_name):

        def check_prop(prop):
            t = type(prop)
            # print(prop, t)
            if t == str or t == int or t == float or t == bool or prop == None:
                return True
            elif t == list and len(prop) >= 1:
                # ne prend pas les liste comprenants elements differents
                tl0 = type(prop[0])
                # print('tl0', tl0)
                if tl0 == str or tl0 == int or tl0 == float or tl0 == bool:
                    print('on the way')
                    return True
                else:
                    return False
            else:
                return False


        print('parsing json')
        with open(file_name) as file:
            data = file.read()
            json_data = json.loads(data)
            for part in json_data:
                for main_prop in part:
                    if type(main_prop) == str or type(main_prop) == int:
                        if check_prop(part[main_prop]):
                            print(main_prop, part[main_prop])
                        else:
                            for second_prop in part[main_prop]:
                                if type(second_prop) == str or type(second_prop) == int:
                                    print('second prop', type(second_prop))
                                    if check_prop(part[main_prop][second_prop]):
                                        print(second_prop, part[main_prop][second_prop])
                                    else:
                                        print('checking for thirs prop')
                                        for third_prop in part[main_prop][second_prop]:
                                            print(third_prop)
                                            if type(third_prop) == str or type(third_prop) == int:
                                                if check_prop(part[main_prop][second_prop][third_prop]):
                                                    print(third_prop, part[main_prop][second_prop][third_prop])
                                                else:
                                                    print('checking for fourth prop')
                                                    for p4 in part[main_prop][second_prop][third_prop]:
                                                        if type(p4) == str or type(p4) == int:
                                                            if check_prop(part[main_prop][second_prop][third_prop][p4]):
                                                                p = part[main_prop][second_prop][third_prop]
                                                                print('4th', p[p4])


                            # print('loop', main_prop, type(part[main_prop]))

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
        print(list)
        self.main_stacked_layout.setCurrentIndex(0)
        self.parent.part_catalog_update()

    def confirm_import(self, list):
        # print('confirming import list')
        self.main_stacked_layout.setCurrentIndex(1)
        self.confirmation_widget.display_import_list(list)


