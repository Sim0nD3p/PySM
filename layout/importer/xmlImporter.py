from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout

from layout.importer.treePropertiesEditor import TreePropretiesEditor
from part.Part import Part
import xml.etree.ElementTree as et


class XmlImporter(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.tree = TreePropretiesEditor()

        self.bottom_buttons = QWidget()
        self.create_bottom_buttons()

        self.create_layout()

    def create_bottom_buttons(self):
        hbox = QHBoxLayout()

        b_auto_fill = QPushButton('should auto-fill')

        b_init_import = QPushButton('Suivant')
        b_init_import.clicked.connect(self.initiate_creation)

        hbox.addWidget(b_auto_fill)
        hbox.addWidget(b_init_import)

        self.bottom_buttons.setLayout(hbox)


    def create_layout(self):
        vbox = QVBoxLayout()

        vbox.addWidget(self.tree)
        vbox.addWidget(self.bottom_buttons)

        self.setLayout(vbox)

    def create_object(self, data, instructions):
        # might be moved in Part class method for custom constructor
        # will need to check for error handling on get and make functions for when the data is not available

        part_code = Part.get_code(data, instructions)
        part = Part(part_code)
        part.general_information = Part.make_general_information(data, instructions)
        part.specifications = Part.make_specifications(data, instructions)

        # will add custom properties
        part = Part.add_custom_prop(part, data, instructions)
        return part

    def initiate_creation(self):
        """
        Initiate the import of parts from xml file
        1. gets instructions from QTreeWidget
        :return:
        """
        # getting instruction to get data in the right path source data -> object
        decoder_instructions = Part.inspect_tree(self.tree.xml_tree.getroot())
        print('Decoder instructions')
        print(decoder_instructions)

        # this is only for testing purpose will be the file selected via explorer
        input_file = et.ElementTree()
        input_file.parse('layout/criss.xml')
        data = input_file.getroot()
        # print('xml data')

        # print(data)
        # we get xml root of the data file from which we will take data for parts

        # instructions of where to get values for each child properties in the partModel
        # decoder_instructions = self.inspect_tree(model=self.tree.xml_tree.getroot())
        # for each part, will need to get all properties with get_instructions_list -> returns all all {path:value}
        # FOR LOOP (for testing, we do only 1 part)

        imported_list = []
        # print(Part.inspect_tree(data[0]))

        for source in data:
            part = self.create_object(Part.inspect_tree(source), decoder_instructions)
            imported_list.append(part)
        # self.parent.get_import_list(imported_list)
        self.parent.confirm_import(imported_list)





        # create_object(self.get_instructions_list(data[0]), decoder_instructions)
        # print(decoder_instructions)
        """
        creation path for specific object"""


