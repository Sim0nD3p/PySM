from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QFrame
from backend.PartCatalog import PartCatalog
from layout.settings.settings import Settings
from part.Part import Part


class FilterWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.resize(500, 200)
        self.setObjectName('filterFrame')
        self.setStyleSheet('QFrame#filterFrame{background-color:#e6e6e6; border:1px solid black}')
        self.main_vbox = QVBoxLayout()




        # search by text
        self.text_edit = QLineEdit()
        self.part_properties_dropdown = QComboBox()
        self.b_submit_search = QPushButton('Rechercher')


        # drop down for type (in settings)
        self.types_dropdown = QComboBox()

        self.draw_filters_content()

        self.setLayout(self.main_vbox)

    def filter_catalog(self):
        """
        Main filter method
        :return:
        """
        t = self.part_properties_dropdown.currentText()
        property_text_filter = self.part_properties_dropdown.itemData(self.part_properties_dropdown.currentIndex())
        results = PartCatalog.filter_path(None, property_text_filter, self.text_edit.text())  # filter about text (first line)

        print(len(results))
        # print(self.types_dropdown.itemData(self.types_dropdown.currentIndex()))
        results = PartCatalog.filter_path(results, Settings.filter_dropdown_types,
                                          self.types_dropdown.itemData(self.types_dropdown.currentIndex()))


        return results


    def draw_filters_content(self):
        """
        Draws elements of the filterWidget
        :return: void
        """
        self.create_text_search()
        self.create_type_filter()
        self.update_properties_dropdown()

    def update_properties_dropdown(self):
        """
        Properties in dropdown for which property to search text
        :return:
        """
        properties = Part.get_default_properties_list()
        self.part_properties_dropdown.clear()

        self.part_properties_dropdown.addItem('tout', userData=properties)
        for prop in properties:
            self.part_properties_dropdown.addItem(prop.split('/')[len(prop.split('/')) - 1], userData=prop)

    def create_text_search(self):
        """
        Creates text search, first line in filterWidget and adds it to main vbox
        :return:
        """
        hbox = QHBoxLayout()
        hbox.addWidget(self.text_edit)
        hbox.addWidget(self.part_properties_dropdown)
        hbox.addWidget(self.b_submit_search)
        self.main_vbox.addLayout(hbox)

    def update_types_dropdown(self):
        """
        Updates the types filter dropdown
        :return: void
        """
        self.types_dropdown.clear()
        self.types_dropdown.addItem('tout', userData=None)
        for type_prop in PartCatalog.get_all_values_instance_for_property(Settings.filter_dropdown_types):
            self.types_dropdown.addItem(type_prop, userData=type_prop)
    def create_type_filter(self):
        """
        Create dropdown selector to filter parts, adds it to main vbox
        :return:
        """
        hbox = QHBoxLayout()
        self.update_types_dropdown()
        hbox.addWidget(QLabel('Filtrer par type:'))
        hbox.addWidget(self.types_dropdown)
        self.main_vbox.addLayout(hbox)


        


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
