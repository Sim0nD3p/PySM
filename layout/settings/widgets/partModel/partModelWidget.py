from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLineEdit, QTreeWidget, QLabel, QTreeWidgetItem, \
    QVBoxLayout
import xml.etree.ElementTree as eT


class PartModelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.file = 'part/partModel.xml'

        self.xml_tree_object = eT.ElementTree()
        self.xml_tree_object.parse(self.file)
        print(self.xml_tree_object)

        self.treewidget = QTreeWidget()
        self.draw_tree()

        self.bottom_buttons = QWidget()
        self.create_bottom_buttons()

        self.text_edit = QLineEdit()
        self.input_widget = QWidget()
        self.create_input_widget()



        self.bottom_widget = QWidget()
        self.create_bottom_widget()

        self.upper_buttons = QWidget()
        self.create_upper_buttons()

        vbox = QVBoxLayout()
        vbox.addWidget(self.upper_buttons)
        vbox.addWidget(self.treewidget)
        vbox.addWidget(self.bottom_widget)
        self.setLayout(vbox)

    def create_upper_buttons(self):
        hbox = QHBoxLayout()

        button1 = QPushButton('button 1')
        button2 = QPushButton('button 2')
        button3 = QPushButton('button 3')
        button4 = QPushButton('button 4')

        hbox.addWidget(button1)
        hbox.addWidget(button2)
        hbox.addWidget(button3)
        hbox.addWidget(button4)

        self.upper_buttons.setLayout(hbox)

    def create_bottom_buttons(self):
        hbox = QHBoxLayout()

        # b_add_prop = QPushButton('Ajouter sous propriété')
        # b_add_prop.clicked.connect(self.add_prop)

        b_sup_prop = QPushButton('Supprimer propriété actuelle')
        b_sup_prop.clicked.connect(self.sup_prop)
        button3 = QPushButton('button 3')
        button4 = QPushButton('button 4')

        # hbox.addWidget(b_add_prop)
        hbox.addWidget(b_sup_prop)
        hbox.addWidget(button3)
        hbox.addWidget(button4)

        self.bottom_buttons.setLayout(hbox)

    def create_input_widget(self):
        hbox = QHBoxLayout()

        label = QLabel('Nom propriété')

        b_add_prop = QPushButton('Ajouter')
        b_add_prop.setEnabled(False)
        b_add_prop.clicked.connect(self.add_prop)

        def enableButton(text):
            print(text)
            if len(text) == 0:
                print('should disable')
                b_add_prop.setEnabled(False)
            else:
                b_add_prop.setEnabled(True)

        self.text_edit.textChanged.connect(enableButton)

        hbox.addWidget(label)
        hbox.addWidget(self.text_edit)
        hbox.addWidget(b_add_prop)
        self.input_widget.setLayout(hbox)


    def create_bottom_widget(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.input_widget)
        vbox.addWidget(self.bottom_buttons)

        self.bottom_widget.setLayout(vbox)


    def draw_tree(self):
        root = self.xml_tree_object.getroot()
        print('root', root.tag)
        widget_root = QTreeWidgetItem([root.tag])
        self.treewidget.setColumnCount(1)
        self.treewidget.addTopLevelItem(widget_root)

        # self.treewidget.openPersistentEditor(item, column)

        def draw_branches(root, xml_element):
            for child in xml_element:
                branch = QTreeWidgetItem([child.tag])
                root.addChild(branch)
                draw_branches(branch, child)

        draw_branches(widget_root, root)
        self.treewidget.expandAll()
        self.treewidget.setCurrentItem(widget_root)

    def add_prop(self):
        new_prop_tag = self.text_edit.text()
        self.text_edit.setText('')

        tree_elements = self.get_tree_element(self.treewidget.currentItem())
        for child in tree_elements:
            e = QTreeWidgetItem([new_prop_tag])
            child.addChild(e)
        element = self.get_xml_element(self.treewidget.currentItem())
        for i in element:
            i.append(eT.Element('new element'))

    def sup_prop(self):
        self.get_xml_element(self.treewidget.currentItem())


    def get_xml_element(self, tree_element):
        def get_parent_path(tree_item):
            def get_parent(item, outstring):
                if item.parent() is None:
                    return outstring
                outstring = item.parent().text(0) + '/' + outstring
                return get_parent(item.parent(), outstring)
            output = get_parent(tree_item, tree_item.text(0))
            return output

        parent_path = get_parent_path(tree_element)
        direct_path = parent_path.lstrip(self.xml_tree_object.getroot().tag + '/')

        return self.xml_tree_object.findall(direct_path)


    def get_tree_element(self, tree_element):
        return self.treewidget.findItems(tree_element.text(0), Qt.MatchFlag.MatchRecursive)





