from PyQt6.QtWidgets import QPushButton

from layout.importer.treePropertiesEditor import TreePropretiesEditor
from part.Part import Part

class TreeInspector(TreePropretiesEditor):
    def __init__(self):
        super().__init__()
        self.submit_button = QPushButton('Suivant')
        self.vbox.addWidget(self.submit_button)

    def get_decoder_instructions(self):
        return Part.inspect_xml_tree(self.xml_tree.getroot())