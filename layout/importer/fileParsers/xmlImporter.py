from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout

from layout.importer.treeInspector import TreeInspector
from layout.importer.treePropertiesEditor import TreePropretiesEditor
from part.Part import Part
import xml.etree.ElementTree as et

class XmlImporter(TreeInspector):
    def __init__(self):
        super().__init__()

    def handle_submit(self):
        print('handle xml')
        decoder_instructions = Part.inspect_xml_tree(self.xml_tree.getroot())
        data_stack = self.get_data()
        return decoder_instructions, data_stack

    def get_data(self):
        # this is only for testing purpose will be the file selected via explorer
        input_file = et.ElementTree()
        input_file.parse('layout/criss.xml')
        data = input_file.getroot()
        data_stack = []

        for child in data:
            child_data = Part.inspect_xml_tree(child)
            data_stack.append(child_data)

        return data_stack