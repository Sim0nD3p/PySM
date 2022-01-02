from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QStackedLayout, \
    QComboBox, QFileDialog, QLineEdit
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
import xml.etree.ElementTree as et
import json
from part.Part import Part
from part.dataClasses import Specifications, GeneralInformation


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


class TreePropretiesEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.template = 'part/partModel.xml'  # template xml file
        self.xml_tree = et.ElementTree()
        self.xml_tree.parse(self.template)

        self.selected_tree_element = None

        self.tree_widget = QTreeWidget()
        self.tree_widget.itemDoubleClicked.connect(self.handle_double_click)
        self.draw_tree()

        self.selected_path = QLabel()
        self.upper_bottom_line_infos = QWidget()
        self.create_upper_bottom_line_infos()

        self.label_prop = QLabel('Chemin source')
        self.text_box = QLineEdit()
        self.b_add_prop = QPushButton('Ajouter')
        self.b_add_prop.setEnabled(False)
        self.b_add_prop.clicked.connect(self.add_prop)
        self.text_box.textChanged.connect(self.set_submit_button_enabled)

        self.input_line = QWidget()
        self.create_input_line()

        self.bottom_widget = QWidget()
        self.create_bottom_widget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tree_widget)
        vbox.addWidget(self.bottom_widget)
        self.setLayout(vbox)


    def draw_tree(self):
        self.tree_widget.setColumnCount(2)
        xml_root = self.xml_tree.getroot()

        widget_root = QTreeWidgetItem([xml_root.tag])
        self.tree_widget.addTopLevelItem(widget_root)

        def create_branches(root, xml_element):
            for child in xml_element:
                branch = QTreeWidgetItem([child.tag, child.text])
                root.addChild(branch)
                create_branches(branch, child)

        create_branches(widget_root, xml_root)
        self.tree_widget.expandAll()
        self.tree_widget.setColumnWidth(0, 200)

    def create_upper_bottom_line_infos(self):
        hbox = QHBoxLayout()
        selected_path_info = QLabel('Chemin sélectionné:')
        selected_path_info.setMaximumWidth(110)
        self.selected_path.setText('')
        font = QFont()
        font.setBold(True)
        self.selected_path.setFont(font)

        hbox.addWidget(selected_path_info)
        hbox.addWidget(self.selected_path)
        self.upper_bottom_line_infos.setLayout(hbox)

    def create_input_line(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_prop)
        hbox.addWidget(self.text_box)
        hbox.addWidget(self.b_add_prop)
        self.input_line.setLayout(hbox)



    def create_bottom_widget(self):
        vbox = QVBoxLayout()
        filler = QLabel('filler')

        bottom_buttons = QWidget()
        hbox = QHBoxLayout()

        b_del_prop = QPushButton('Supprimer lien')
        b_submit_template = QPushButton('Write XML template')
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')

        b_del_prop.clicked.connect(self.delete_prop)
        b_submit_template.clicked.connect(self.submit_template)

        hbox.addWidget(b_del_prop)
        hbox.addWidget(b_submit_template)
        hbox.addWidget(button3)
        hbox.addWidget(button4)

        bottom_buttons.setLayout(hbox)

        vbox.addWidget(self.upper_bottom_line_infos)
        vbox.addWidget(self.input_line)
        vbox.addWidget(bottom_buttons)

        self.bottom_widget.setLayout(vbox)

    def get_path(self, element, delimiter):
        """
        Gets path of tree element
        :param element: elementTree.ElementTree.Element
        :param delimiter:
        :return:
        """
        def get_parent_path(tree_item):
            def get_parent(item, outstring):
                if item.parent() is None:
                    return outstring
                outstring = item.parent().text(0) + delimiter + outstring
                return get_parent(item.parent(), outstring)
            output = get_parent(tree_item, tree_item.text(0))
            return output
        final_path = get_parent_path(element)
        return final_path

    def get_xml_element(self, path):
        direct_path = path[path.find('/')+1:]
        return self.xml_tree.findall(direct_path)

    def handle_double_click(self, tree_element):
        if tree_element.childCount() == 0:
            self.selected_tree_element = tree_element
            full_path = self.get_path(tree_element, '/')
            self.selected_path.setText(full_path)
            self.text_box.setText(tree_element.text(1))

    def add_prop(self):
        if self.selected_tree_element is not None:
            self.selected_tree_element.setText(1, self.text_box.text())
            full_path = self.get_path(self.selected_tree_element, '/')
            xml_element = self.get_xml_element(full_path)[0]
            print(xml_element)
            xml_element.text = self.text_box.text()

    def delete_prop(self):
        if self.selected_tree_element is not None:
            self.selected_tree_element.setText(1, '')
            self.text_box.setText('')
            full_path = self.get_path(self.selected_tree_element, '/')
            xml_element = self.get_xml_element(full_path)[0]
            xml_element.text = ''

    def set_submit_button_enabled(self, text):
        if len(text) > 0:
            self.b_add_prop.setEnabled(True)
        else:
            self.b_add_prop.setEnabled(False)

    def submit_template(self):
        print('submit template')
        self.xml_tree.write('output.xml')


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




class JsonImporter(QWidget):
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

        b_auto_fill = QPushButton('useless button')

        button = QPushButton('button')
        button.clicked.connect(self.initiate_creation)

        hbox.addWidget(b_auto_fill)
        hbox.addWidget(button)

        self.bottom_buttons.setLayout(hbox)


    def create_layout(self):
        vbox = QVBoxLayout()

        vbox.addWidget(self.tree)
        vbox.addWidget(self.bottom_buttons)

        self.setLayout(vbox)

    def inspect_tree(self, model):
        """
        Returns the path of all child element and their text value in xml tree
        :param model: xml.ElementTree.Element to return child properties
        :return: dict(path:value)
        """
        rec = {}
        def loop(branch, path):
            def get_path(root, p):
                if len(root) == 0:  # when element has no child, we return the element and its path
                    pa = path + '/' + root.tag
                    val = root.text
                    en = [pa, val]
                    return en
                else:   # if element has child, we loop trough them
                    p = p + '/' + root.tag
                    loop(root, p)

            for child in branch:    # for every element in the branch
                value = get_path(child, path)
                if value is not None:
                    rec[value[0]] = value[1]

        loop(model, model.tag)
        return rec

    def add_custom_props(self, part, data, instructions):
        for object_path in instructions:            # go trough all the properties path of the partModel
            object_dir = object_path.split('/')     # split path directions
            common_types = ['code', 'general_information', 'specifications']
            if object_dir[1] not in common_types:   # excludes common types to only get custom properties
                value = None
                if instructions[object_path] in data:   # if we have data with corresponding path given by instructions
                    # the instructions give {partModel path(object path): data path}
                    source_path = instructions[object_path]
                    value = data[source_path]

                def go_to_element(current_part, path, current_value):
                    placeholder = current_part
                    for i in range(len(path)):
                        if i > 0:
                            if hasattr(placeholder, '__dict__'):
                                if i == len(path) - 1:
                                    placeholder.__setattr__(path[i], current_value)
                                else:
                                    placeholder_child_value = {}
                                    if hasattr(placeholder, path[i]):
                                        placeholder_child_value = placeholder.__getattribute__(path[i])
                                    placeholder.__setattr__(path[i], placeholder_child_value)
                                    placeholder = placeholder.__getattribute__(path[i])
                            else:
                                if i == len(path) - 1:
                                    placeholder[path[i]] = current_value
                                    return current_part
                                else:
                                    if path[i] not in placeholder:
                                        placeholder[path[i]] = {path[i + 1]: 'something'}
                                    placeholder = placeholder[path[i]]

                part = go_to_element(part, object_dir, value)
        return part



    def create_object(self, data, instructions):
        # might be moved in Part class method for custom constructor
        # will need to check for error handling on get and make functions for when the data is not available
        def get_code(data, instructions):
            path = {'code': 'part/code'}

            code = data[instructions[path['code']]]

            return code

        def make_data_specs(data, instructions):
            """
            Takes data dictionary and instructions dictionary and returns specifications dataclass.
            The function go search the data with the path of the property found in the instructions dictionary
            :param data:
            :param instructions:
            :return: Specifications dataclass
            """
            paths = {  # This is the paths of specifications in partModel, where
                'length': 'part/specifications/length',
                'width': 'part/specifications/width',
                'height': 'part/specifications/height',
                'weight': 'part/specifications/weight'
            }
            length = data[instructions[paths['length']]]
            width = data[instructions[paths['width']]]
            height = data[instructions[paths['height']]]
            weight = data[instructions[paths['weight']]]

            return Specifications(length=length, width=width, height=height, weight=weight)

        def make_general_informations(data, instructions):
            """
            Takes data dictionary and instructions dictionary and returns GeneralInformation dataclass.
            The function go search the data with the path of the property found in the instructions dictionary
            :param data:
            :param instructions:
            :return: GeneralInformation dataClass
            """
            paths = {
                'description': 'part/general_information/description'
            }
            description = data[instructions[paths['description']]]

            return GeneralInformation(description=description)

        # print('this is instructions')
        # print(instructions)

        # print('this is data')
        # print(data)

        part_code = get_code(data, instructions)
        part = Part(part_code)
        part.general_information = make_general_informations(data, instructions)
        part.specifications = make_data_specs(data, instructions)

        # will add custom properties
        part = self.add_custom_props(part, data, instructions)
        return part

        # print(help(part))
        # print(part.__dict__)

    def initiate_creation(self):

        # this is only for testing purpose will be the file selected via explorer
        input_file = et.ElementTree()
        input_file.parse('layout/criss.xml')
        data = input_file.getroot()
        # we get xml root of the data file from which we will take data for parts

        # instructions of where to get values for each child properties in the partModel
        decoder_instructions = self.inspect_tree(model=self.tree.xml_tree.getroot())

        # for each part, will need to get all properties with get_instructions_list -> returns all all {path:value}
        # FOR LOOP (for testing, we do only 1 part)

        imported_list = []

        for source in data:
            part = self.create_object(self.inspect_tree(source), decoder_instructions)
            imported_list.append(part)
        self.parent.get_import_list(imported_list)





        # create_object(self.get_instructions_list(data[0]), decoder_instructions)
        # print(decoder_instructions)
        """
        creation path for specific object"""










class Importer(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.types = ['csv', 'json', 'xml']
        self.parent = parent
        self.csv_importer = QLabel('csv')
        self.json_importer = JsonImporter(parent=self)
        self.xml_importer = XmlImporter(parent=self)


        self.stacked_widget = QWidget()
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.csv_importer)
        self.stacked_layout.addWidget(self.json_importer)
        self.stacked_layout.addWidget(self.xml_importer)
        self.stacked_widget.setLayout(self.stacked_layout)

        self.selection = typeSelection(parent=self)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.selection)
        self.hbox.addWidget(self.stacked_widget)
        self.setLayout(self.hbox)

    def change_import_window(self, type):
        print('change import window')
        index = self.types.index(type)
        self.stacked_layout.setCurrentIndex(index)

    def update_import_window(self, file_name, file_type):
        print('update import window')
        if file_type == 'json':
            self.json_importer.update_tree(file_name)

    def get_import_list(self, list):
        print(list)
        self.parent.handle_part_import(list)

