from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QStackedLayout, \
    QTabWidget
from layout.importer.confirmationWidget import ConfirmationWidget
from layout.importer.catalogInputModules.part_importer import PartImporter
from PyQt6.QtCore import Qt
from backend.PartCatalog import PartCatalog
from layout.importer.catalogInputModules.props_importer import PropsImporter
from layout.importer.catalogInputModules.history_importer import HistoryImporter


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
    """
    has catalogInputModules and confirmation widget, acts on them
    """
    def __init__(self):
        super().__init__()
        self.main_stack_layout = QStackedLayout()
        self.tab_widget = QTabWidget()

        # PART IMPORTER
        self.part_importer = PartImporter(parent=self)
        self.part_importer.json_importer.submit_button.clicked.connect(lambda: self.trigger_confirmation('part',
            self.part_importer.get_data_from_importer('JSON')))

        self.part_importer.xml_importer.submit_button.clicked.connect(lambda: self.trigger_confirmation('part',
            self.part_importer.get_data_from_importer('xml')))

        # PROPS IMPORTER
        self.props_importer = PropsImporter()
        self.props_importer.json_importer.submit_button.clicked.connect(lambda: self.trigger_confirmation('prop',
            self.props_importer.get_data_from_importer('JSON')
        ))
        self.props_importer.xml_importer.submit_button.clicked.connect(lambda: self.trigger_confirmation('prop',
            self.props_importer.get_data_from_importer('xml')
        ))

        # HISTORY IMPORTER
        self.history_importer = HistoryImporter()
        self.history_importer.submit_button.clicked.connect(self.history_importer.make_order_pool)


        self.tab_widget.addTab(self.part_importer, 'Pi??ce')
        self.tab_widget.addTab(self.props_importer, 'Propri??t??')
        self.tab_widget.addTab(self.history_importer, "Historique d'achats")
        self.main_stack_layout.addWidget(self.tab_widget)

        self.confirmation_widget = ConfirmationWidget()
        self.confirmation_widget.confirm_button.clicked.connect(self.submit_import)
        self.main_stack_layout.addWidget(self.confirmation_widget)

        self.setLayout(self.main_stack_layout)

    def test(self):
        print('caliss')

    def submit_import(self):
        """
        gets what to do with which parts from confirmationWidget
        for each importer (part, props), there are 2 possibilities:
            - part is absent in database
            - part is present in database


        when importing parts:
            - absent: creating part
            - present: merging, replacing or ignore
            checkbox:
                - merge: importing prop -> could be replaced by import props
                - replacing: delete and create
                - ignore: do nothing


        when importing props:
            - absent: ignore or create part
            - present: importing props (replacing them by default)


        :return:
        """
        print('submit import')
        print('filtering parts')
        present = self.confirmation_widget.tree.topLevelItem(0)
        absent = self.confirmation_widget.tree.topLevelItem(1)
        # if we import new parts
        if self.tab_widget.currentIndex() == 0:
            # looping thru already present parts
            for index in range(present.childCount()):   # loop thru present
                data = present.child(index).data(1, 1)
                if present.child(index).checkState(1) == Qt.CheckState.Checked:
                    # checked present
                    # replace part
                    print('present checked')
                    PartCatalog.remove_part(data['part/code'])
                else:
                    # unchecked present
                    # do nothing (dont import part)
                    print('present unchecked')
            for index in range(absent.childCount()):    # loop thru absent
                data = absent.child(index).data(1, 1)
                instructions = absent.child(index).data(1, 2)
                if absent.child(index).checkState(1) == Qt.CheckState.Checked:
                    # checked absent
                    # import part
                    self.part_importer.import_part(instructions, data)
                else:
                    # unchecked absent
                    # do nothing
                    print('absent unchecked')
        elif self.tab_widget.currentIndex() == 1:  # import props
            for index in range(present.childCount()):   # loop thru present
                data = present.child(index).data(1, 1)
                instructions = present.child(index).data(1, 2)
                if present.child(index).checkState(1) == Qt.CheckState.Checked:
                    # checked present
                    # add props to part
                    self.props_importer.import_props_to_part(instructions, data)

                else:
                    # unchecked present
                    print('test')
            for index in range(absent.childCount()):    # loop thru absent
                # data = absent.child(index)
                if absent.child(index).checkState(1) == Qt.CheckState.Checked:
                    # checked absent
                    print('test')
                else:
                    # unchecked absent
                    print('test')
                # data = absent.child(index)
        elif self.tab_widget.currentIndex() == 2:
            # importing history
            print('import history')


        print(present.childCount())

    def get_decoder_instructions(self, data_type):
            instructions, data = self.part_importer.get_data_from_importer(data_type)



    def trigger_confirmation(self, confirmation_type, data):
        """
        calls the confirmationWidget
        :param data: (decoder_instructions, data)
        :return:
        """
        decoder_instructions, data = data
        print('show confirm')
        self.confirmation_widget.update_tree(confirmation_type, data, decoder_instructions)
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
        self.tab_widget.addTab(self.part_importer, 'Importer pi??ces')
        self.tab_widget.addTab(self.props_pusher, 'Impoter propri??t??')



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



