import sys

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, \
    QStackedLayout, QLineEdit
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtWidgets import QApplication
import xml.etree.ElementTree as et

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setGeometry(100, 100, 500, 500)

    def open_window(self, window):
        settings = Settings()
        window.setCentralWidget(settings)
        window.setGeometry(200, 100, 900, 500)
        window.setWindowTitle('Settings')


"""
    Gestion des fichiers:
        -
    Pour les pieces:
        - proprietes de piece (selon modele predefini)
        - 
    Magasin
"""
class PartModelWidgetOld(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.buttons_box = QWidget()
        hbox = QHBoxLayout()

        self.add_element_button = QPushButton('button 1')
        hbox.addWidget(self.add_element_button)
        self.add_element_button.clicked.connect(self.buttonClicked)

        self.write_xml_button = QPushButton('write')
        hbox.addWidget(self.write_xml_button)
        self.write_xml_button.clicked.connect(self.write_xml)

        self.buttons_box.setLayout(hbox)

        self.selected_item = None

        self.treewidget = QTreeWidget()
        hbox = QHBoxLayout()
        f = open('test.xml', 'r').read()

        vbox.addWidget(self.treewidget)
        vbox.addWidget(self.buttons_box)
        self.printtree(f)
        self.setLayout(vbox)

    def buttonClicked(self):
        print('button clicked')
        item = self.treewidget.currentItem()
        newitem = QTreeWidgetItem(['test'])
        item.addChild(newitem)

        p = self.get_parent_path(item)
        element = self.get_tree_element(p)
        element.append(et.Element('New element'))
        print(type(self.tree))

    def write_xml(self):
        tree = et.ElementTree()
        tree.parse('tes2.xml')
        print(tree)
        r = tree.getroot()
        for child in r:
            element = et.Element('Helmet')
            element.text = 'testtt'
            child.append(element)
        tree.write('output.xml')



    def get_parent_path(self, item):
        def get_parent(item, outstring):
            if item.parent() is None:
                return outstring
            outstring = item.parent().text(0) + '/' + outstring
            return get_parent(item.parent(), outstring)
        output = get_parent(item, item.text(0))
        return output

    def get_tree_element(self, path):
        fp = path.lstrip(self.tree.tag + '/')
        element = self.tree.find(fp, namespaces=None)
        return element




    def printtree(self, s):
        print('printtree')
        self.tree = et.fromstring(s)
        self.tree.append(et.Element('TEST'))
        self.treewidget.setColumnCount(1)
        a = QTreeWidgetItem([self.tree.tag])
        self.treewidget.addTopLevelItem(a)

        def display_tree(a, s):
            """
            :param a: QTreeWidgetItem
            :param s: XML element from the tree
            :return:
            """
            for child in s:
                branch = QTreeWidgetItem([child.tag])
                a.addChild(branch)
                display_tree(branch, child)

            # if s.text is not None:
               # content = s.text
               # a.addChild(QTreeWidgetItem([content]))

        display_tree(a, self.tree)


class PartModelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.file = 'partModel.xml'

        self.xml_tree_object = et.ElementTree()
        self.xml_tree_object.parse(self.file)

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
            i.append(et.Element('new element'))

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












class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.categories = ['Général', 'Modèle des pièces', 'Fournisseurs', 'Magasin']
        # self.setGeometry(50, 50, 200, 200)
        self.glo = 0
        self.part_model_widget = PartModelWidget()
        # self.create_list()
        self.category_index = 0
        self.create_layout(self.category_index)

    def create_list(self):
        self.list = QListWidget(self)
        for category in self.categories:
            self.list.addItem(category)
        self.list.itemClicked.connect(self.test)

    def create_layout(self, category_index):
        # print(str(self.category_index))
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()


        self.create_list()
        self.stackedLayout = QStackedLayout()
        wid1 = QLabel('this is a label')
        wid1.setStyleSheet('background-color:red')

        wid2 = QLabel('this is another label')
        wid2.setStyleSheet('background-color:blue')

        wid3 = QLabel('this is another label')
        wid3.setStyleSheet('background-color:green')

        wid4 = QLabel('this is another label')
        wid4.setStyleSheet('background-color:yellow')


        self.stackedLayout.addWidget(wid1)
        self.stackedLayout.addWidget(self.part_model_widget)
        self.stackedLayout.addWidget(wid3)
        self.stackedLayout.addWidget((wid4))


        self.widget = QWidget()
        self.widget.setLayout(self.stackedLayout)
        hbox.addWidget(self.list)
        hbox.addWidget(self.widget)


        self.setLayout(hbox)

    def test(self, e):
        print('this is a test', e)
        index = self.categories.index(e.text())
        self.stackedLayout.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())

