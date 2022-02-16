from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLineEdit, QTreeWidget, QLabel, QTreeWidgetItem, \
    QVBoxLayout, QMainWindow
import xml.etree.ElementTree as eT
from layout.settings.widgets.partModel.PartModelTreeEditor import PartModelTreeEditor




class PartModelWidget(QWidget):
    """
    All settings regarding partModel
    - select partModel file
    - select root name for part
    """
    def __init__(self):
        super().__init__()
        self.main_vbox = QVBoxLayout()

        self.treeWindow = QMainWindow()
        self.tree = PartModelTreeEditor()

        self.root_name_edit = QLineEdit()




        b_part_editor = QPushButton('Modifier la structure de pièce')
        b_part_editor.clicked.connect(self.handleClick)

        self.main_vbox.addWidget(b_part_editor)
        self.create_layout()


    def create_settings(self):
        """
        Create all settings for partModel
        :return:
        """
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('Modifier racine pièce (root)'))




    def handleClick(self):
        print('handle click')
        self.treeWindow.setGeometry(200, 200, 400, 400)
        self.treeWindow.setCentralWidget(self.tree)
        self.treeWindow.show()

    def create_layout(self):
        # self.main_vbox.addWidget()
        self.setLayout(self.main_vbox)



class PartModelWidget_old(QWidget):
    def __init__(self):
        super().__init__()
        self.treeWindow = QMainWindow()
        self.file = 'backend/appData/partModels/partModel.xml'

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


        vbox = QVBoxLayout()
        vbox.addWidget(self.treewidget)
        vbox.addWidget(self.bottom_widget)
        self.setLayout(vbox)



    def create_bottom_buttons(self):
        hbox = QHBoxLayout()

        # b_add_prop = QPushButton('Ajouter sous propriété')
        # b_add_prop.clicked.connect(self.add_prop)

        b_sup_prop = QPushButton('Supprimer propriété actuelle')
        b_sup_prop.clicked.connect(self.sup_prop)
        button3 = QPushButton('(save as)')

        b_save = QPushButton('Enregistrer')
        b_save.clicked.connect(self.save_part_model)

        # hbox.addWidget(b_add_prop)
        hbox.addWidget(b_sup_prop)
        hbox.addWidget(button3)
        hbox.addWidget(b_save)

        self.bottom_buttons.setLayout(hbox)


    def save_part_model(self):
        print('saving part model')
        self.xml_tree_object.write('backend/appData/partModels/partModel.xml')

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
        print(tree_elements)
        for child in tree_elements:
            e = QTreeWidgetItem([new_prop_tag])
            child.addChild(e)
        element = self.get_xml_element(self.treewidget.currentItem())
        # print('xml element', element)
        # print(self.xml_tree_object.getroot())
        if len(element) > 0:
            for i in element:
                i.append(eT.Element(new_prop_tag))
        else:
            self.xml_tree_object.getroot().append(eT.Element(new_prop_tag))

    def sup_prop(self):
        print('current item', self.treewidget.currentItem())
        element = self.get_xml_element(self.treewidget.currentItem())
        path = self.get_parent_path(self.treewidget.currentItem())
        parent_path = path[:len(path) - len(path.split('/')[len(path.split('/')) - 1])-1]
        direct_path = parent_path[len(parent_path.split('/')[0])+1:]
        xml_parent = self.xml_tree_object.findall(direct_path)
        if len(xml_parent) != 0:
            for xml_element in xml_parent:
                xml_element.remove(element[0])
                print(element[0])
        else:
            self.xml_tree_object.getroot().remove(element[0])

        tree_elements = self.get_tree_element(self.treewidget.currentItem())
        for element in tree_elements:
            parent_element = element.parent()
            parent_element.removeChild(element)


    def get_parent_path(self, tree_item):
        """
        Gets path of a QTreeWidgetItem
        :param tree_item: QTreeWidgetItem
        :return: path
        """
        def get_parent(item, outstring):
            if item.parent() is None:
                return outstring
            outstring = item.parent().text(0) + '/' + outstring
            return get_parent(item.parent(), outstring)

        output = get_parent(tree_item, tree_item.text(0))
        return output

    def get_xml_element(self, tree_element):
        """
        Gets the xml element associated with the QTreeWidgetItem given
        :param tree_element: QTreeWidgetItem
        :return: xml.etree.ElementTree.Element
        """
        parent_path = self.get_parent_path(tree_element)
        direct_path = parent_path[len(parent_path.split('/')[0])+1:]

        return self.xml_tree_object.findall(direct_path)


    def get_tree_element(self, tree_element):
        """
        Gets the QTreeWidgetItem element in the QTreeWidget
        :param tree_element:
        :return: QTreeWidgetItem
        """
        return self.treewidget.findItems(tree_element.text(0), Qt.MatchFlag.MatchRecursive)





