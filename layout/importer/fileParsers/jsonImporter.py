from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTreeWidget, QTreeWidgetItem
from layout.importer.treePropertiesEditor import TreePropretiesEditor
from layout.importer.treeInspector import TreeInspector
import json
from layout.settings.settings import Settings
from part.Part import Part

class JsonImporter(TreeInspector):
    def __init__(self):
        super().__init__()

    def handle_submit(self):
        """
        gets decoder_instructions and data dict to create object and returns it
        :return: decoder_instructions, object_data
        """
        decoder_instructions = Part.inspect_xml_tree(self.xml_tree.getroot())
        data_stack = self.get_data()

        return decoder_instructions, data_stack

    def get_data(self):
        data_stack = []
        file_name = 'PFEPtest.json'
        with open(file_name) as json_string:
            json_data = json.load(json_string)
            for child in json_data:
                data = Part.inspect_json_tree(child, Settings.json_part_root)
                data_stack.append(data)
        return data_stack
