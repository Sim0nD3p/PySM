from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedLayout
from layout.importer.file_selector import FileSelector
from layout.importer.jsonImporter import JsonImporter
from layout.importer.treeInspector import TreeInspector
from layout.importer.xmlImporter import XmlImporter
from part.Part import Part
from backend.PartCatalog import PartCatalog



class Importer(QWidget):
    """
    Gets the data and instructions needed to make part objects
    receivendata and instructions from importers(xml, json) and its child will either make new catalog or update /
    catalog props

    """

    def __init__(self, parent=None):
        super().__init__()
        self.file_types = ['json', 'csv', 'xml']
        self.parent = parent

        self.xml_importer = XmlImporter()
        self.json_importer = JsonImporter()
        self.csv_importer = QLabel('csv importer placeholder')

        # triggers for next step
        # self.json_importer.submit_button.clicked.connect(lambda: self.confirm_import('JSON'))
        # self.xml_importer.submit_button.clicked.connect(lambda: self.confirm_import('xml'))

        self.file_selector = FileSelector(parent=self, file_types=self.file_types)
        self.file_selector.dropdown.currentIndexChanged.connect(self.handle_filetype_change)

        self.importer_stack_layout = QStackedLayout()

        self.create_importer_stack()
        self.create_layout()

    def test(self):
        print('this is test from importer')


    def create_importer_stack(self):
        self.importer_stack_layout.addWidget(self.json_importer)
        self.importer_stack_layout.addWidget(self.csv_importer)
        self.importer_stack_layout.addWidget(self.xml_importer)


    def create_layout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.file_selector)
        hbox.addLayout(self.importer_stack_layout)

        self.setLayout(hbox)

    def handle_filetype_change(self, index):
        self.importer_stack_layout.setCurrentIndex(index)

    def get_data_from_importer(self, input_datatype):
        # do things according to type might move to Importer
        # gets data and instructions from jsonImporter or xmlImporter, deals with it according to type (see also
        # propsLoader)
        print('import type', input_datatype)
        print('long reach')
        if input_datatype == 'JSON':
            decoder_instructions, data = self.json_importer.handle_submit()
            return decoder_instructions, data
        elif input_datatype == 'xml':
            decoder_instructions, data = self.xml_importer.handle_submit()
            return decoder_instructions, data


class PartImporter(Importer):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        # might move directly in Importer


    def import_part(self, instructions, data):
        part_code = Part.get_code(data, instructions)
        part = Part(part_code)
        part.general_information = Part.make_general_information(data, instructions)
        part.specifications = Part.make_specifications(data, instructions)
        part.add_custom_prop(part, data, instructions)
        PartCatalog.add_part(part)


    def create_object_batch(self, data, instructions):
        print('should start creating batch objects')



    # part creation
    def create_object(self, data, instructions):
        part_code = Part.get_code(data, instructions)
        part = Part(part_code)
        part.general_information = Part.make_general_information(data, instructions)
        part.specifications = Part.make_specifications(data, instructions)
        part = Part.add_custom_prop(part, data, instructions)
        return part






