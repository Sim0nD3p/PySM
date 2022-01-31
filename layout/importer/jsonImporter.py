from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTreeWidget, QTreeWidgetItem
from layout.importer.treePropertiesEditor import TreePropretiesEditor
from layout.importer.treeInspector import TreeInspector
import json

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
                data = Part.inspect_json_tree(child, 'part')
                data_stack.append(data)
        return data_stack


class JsonImporter_old(QWidget):
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


    def create_object(self, data, instructions):
        part_code = Part.get_code(data, instructions)
        part = Part(part_code)
        part.general_information = Part.make_general_information(data, instructions)
        part.specifications = Part.make_specifications(data, instructions)
        part = Part.add_custom_prop(part, data, instructions)
        return part


    # could move with tree_inspector in Part static method sml and json versions different
    def scan_obj(self, obj, root):
        rec = {}

        def scan(obj, root):
            for child in obj:
                if len(root) > 0:
                    new_root = root + '/' + child
                else:
                    new_root = child

                if type(obj[child]) == dict:
                    scan(obj[child], new_root)
                else:
                    rec[new_root] = obj[child]
                    # print(new_root, obj[child])

        scan(obj, root)
        return rec


    def initiate_import(self):
        decoder_instructions = Part.inspect_xml_tree(self.tree.xml_tree.getroot())
        print('Decoder instructions')
        print(decoder_instructions)
        file_name = 'PFEPtest.json'




        imported_list = []
        with open(file_name) as json_string:
            json_data = json.load(json_string)
            for child in json_data:
                #print(child)
                data = self.scan_obj(child, 'part')
                imported_list.append(self.create_object(data, decoder_instructions))



        self.parent.confirm_import(imported_list)
        # code = Part.get_code(json_data, data)
        # part = Part(code)

        # part = Part.add_custom_prop(part, rec, decoder_instructions)
        # imported_list.append(part)
        # print(vars(part))
        # print(code)





