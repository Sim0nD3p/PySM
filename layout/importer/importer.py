from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QStackedLayout, \
    QComboBox, QFileDialog, QTabWidget
import json
from layout.importer.treePropertiesEditor import TreePropretiesEditor
from layout.importer.xmlImporter import XmlImporter
from layout.importer.jsonImporter import JsonImporter
from layout.importer.confirmationWidget import ConfirmationWidget
from layout.importer.new_parts.part_importer import PartImporter
from layout.importer.add_props.props_pusher import PropsPusher
from layout.importer.treePropertiesEditor import TreePropretiesEditor


class ImporterWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.importer = newWidget()

    def open_window(self, window):
        window.setCentralWidget(self.importer)
        self.importer.main_stack_layout.setCurrentIndex(0)
        window.setGeometry(200, 100, 900, 500)
        window.setWindowTitle('Importer catalogue')




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

class newWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.main_stack_layout = QStackedLayout()
        self.tab_widget = QTabWidget()

        self.part_importer = PartImporter(parent=self)
        self.tab_widget.addTab(self.part_importer, 'part')

        self.main_stack_layout.addWidget(self.tab_widget)

        self.confirmation_widget = ConfirmationWidget()
        self.confirmation_widget.confirm_button.clicked.connect(self.submit_import)
        self.main_stack_layout.addWidget(self.confirmation_widget)

        self.setLayout(self.main_stack_layout)


    def submit_import(self):
        print('submit import')
        for i in range(self.confirmation_widget.tree.topLevelItemCount()):
            for j in range(self.confirmation_widget.tree.topLevelItem(i).childCount()):
                print(self.confirmation_widget.tree.topLevelItem(i).child(j))


    def test(self, data):
        print('show confirm')
        self.confirmation_widget.update_tree(data)
        self.main_stack_layout.setCurrentIndex(1)





class Importer_new(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('button', self)

    def test(self):
        print('this is test')

class PI(QWidget):
    def __init__(self):
        super().__init__()
        self.button.clicked.connect(self.handle)

    def handle(self):
        print('shit works')





class Importer_old(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.types = ['csv', 'json', 'xml']
        self.parent = parent

        # child widgets
        self.part_importer = PartImporter(parent=self)
        self.props_pusher = PropsPusher()
        self.confirmation_widget = ConfirmationWidget(parent=self)

        # tabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.part_importer, 'Importer pièces')
        self.tab_widget.addTab(self.props_pusher, 'Impoter propriété')



        self.main_stack = QStackedLayout()
        self.main_stack.addWidget(self.tab_widget)
        self.main_stack.addWidget(self.confirmation_widget)

        self.setLayout(self.main_stack)


    def main_update(self):
        """
        calls the main.py file to update UI
        :param list:
        :return:
        """
        # print(list)
        self.main_stack.setCurrentIndex(0)
        self.parent.part_catalog_update()


    def confirm_import(self, list):
        """
        Deals with all import types, calls confirmation widget
        :param list:
        :return:
        """
        # print('confirming import list')
        self.main_stack.setCurrentIndex(1)
        self.confirmation_widget.display_import_list(list)



