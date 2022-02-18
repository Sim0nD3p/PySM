from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QTreeWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QTreeWidgetItem, \
    QHBoxLayout
import xml.etree.ElementTree as et
from layout.settings.settings import Settings


class TreePropretiesEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.template = Settings.part_model_path  # template xml file
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
        self.add_prop_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.add_prop_shortcut.activated.connect(self.add_prop)
        self.text_box.textChanged.connect(self.set_submit_button_enabled)

        self.input_line = QWidget()
        self.create_input_line()

        self.bottom_widget = QWidget()
        self.create_bottom_widget()

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree_widget)
        self.vbox.addWidget(self.bottom_widget)
        self.setLayout(self.vbox)


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
            self.text_box.setFocus()

    def add_prop(self):
        print(self.selected_tree_element)
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
            self.add_prop_shortcut.setEnabled(True)
        else:
            self.b_add_prop.setEnabled(False)
            self.add_prop_shortcut.setEnabled(False)

    def submit_template(self):
        print('submit template')
        self.xml_tree.write(Settings.part_model_path)
