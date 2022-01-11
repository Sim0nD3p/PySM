from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTreeWidget, QTreeWidgetItem
from layout.importer.treePropertiesEditor import TreePropretiesEditor
import json

from part.Part import Part

class JsonImporter(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.tree = TreePropretiesEditor()
        self.bottom_buttons = QWidget()
        self.create_bottom_buttons()

        self.create_layout()




    def create_layout(self):
        vbox = QVBoxLayout()

        vbox.addWidget(self.tree)
        vbox.addWidget(self.bottom_buttons)

        self.setLayout(vbox)

    def create_bottom_buttons(self):
        hbox = QHBoxLayout()

        b_init_import = QPushButton('Suivant')
        b_init_import.clicked.connect(self.initiate_import)

        label = QLabel('this is a label')
        hbox.addWidget(label)
        hbox.addWidget(b_init_import)
        self.bottom_buttons.setLayout(hbox)

    def initiate_import(self):
        decoder_instructions = Part.inspect_tree(self.tree.xml_tree.getroot())
        print('Decoder instructions')
        print(decoder_instructions)
        file_name = 'sample.json'

        rec = {}

        def scan(obj, root):
            # print('obj', obj, type(obj))
            for child in obj:
                new_root = root + '/' + child
                if type(obj[child]) == dict:
                    scan(obj[child], new_root)
                else:
                    rec[new_root] = obj[child]
                    # print(new_root, obj[child])



        with open(file_name) as json_string:
            json_data = json.load(json_string)
            # print(json_data)
            scan(json_data, 'root')

        print(rec)


        print('testt')




