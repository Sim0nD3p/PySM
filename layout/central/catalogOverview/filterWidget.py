from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from backend.PartCatalog import PartCatalog
from layout.settings.settings import Settings

class FilterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 200)
        self.setStyleSheet('background-color:#bababa')
        self.main_vbox = QVBoxLayout()

        # search by text
        self.text_edit = QLineEdit()
        self.create_text_search()

        # drop down for type (in settings)
        self.dropdown = QComboBox()
        self.create_type_filter()

        self.setLayout(self.main_vbox)

    def create_text_search(self):
        hbox = QHBoxLayout()
        search_label = QLabel('Rechercher: ')
        hbox.addWidget(search_label)
        hbox.addWidget(self.text_edit)
        self.main_vbox.addLayout(hbox)

    def create_type_filter(self):
        print('create type filter')
        PartCatalog.get_all_values_instance_for_property(Settings.dropdown_filter_property)


        


class FilterWidget_old(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(500, 200)
        self.parent = parent
        self.setStyleSheet('background-color:blue')

        self.search_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.search_shortcut.activated.connect(self.submit_search)

        self.text_search = QWidget()
        self.line_edit = QLineEdit()

        self.b_search = QPushButton('soumettre')
        self.b_search.clicked.connect(self.submit_search)

        self.second_line = QWidget()
        self.dropdown = QComboBox()
        self.create_second_line()

        self.create_text_search()
        self.create_layout()

    def submit_search(self):
        print('shoudl search')
        text = self.line_edit.text()
        results = PartCatalog.text_search(None, text)
        print(len(results))
        self.parent.list_widget.draw_list(results)


    def create_text_search(self):
        hbox = QHBoxLayout()
        # hbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Rechercher')
        hbox.addWidget(label)
        hbox.addWidget(self.line_edit)
        hbox.addWidget(self.b_search)
        self.text_search.setLayout(hbox)

    def update_dropdown(self):
        print('updating dropdown')
        print(len(PartCatalog.get_catalog()))
        types_list = PartCatalog.get_all_types()
        self.dropdown.clear()
        self.dropdown.addItems(types_list)

    def create_second_line(self):
        hbox = QHBoxLayout()


        self.dropdown.clear()
        self.dropdown.setMaximumWidth(150)
        l_type = QLabel('Type')

        hbox.addWidget(l_type)
        hbox.addWidget(self.dropdown)

        self.second_line.setLayout(hbox)




    def create_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.text_search)

        label = QPushButton('test')
        label.clicked.connect(self.test)
        vbox.addWidget(self.second_line)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

    def test(self):
        print('testing')
        PartCatalog.get_all_types()
