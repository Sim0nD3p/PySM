import PyQt6.QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from backend.PartCatalog import*
from elements.part.Part import *
from elements.shelf.shelf import *


class PartSelector(QWidget):
    part_selection_signal = pyqtSignal(str, name='part_selection')

    catalog_present = 'Pièce présente dans catalogue'
    catalog_absent = 'Pièce absente du catalogue'
    invalid_code = 'Pièce non valide'

    def __init__(self):
        super().__init__()
        self.completer = QCompleter(PartCatalog.part_list())
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Pièce')
        self.input = QLineEdit()
        self.input.textChanged.connect(self.handle_part_search)

        self.input.setCompleter(self.completer)
        self.submit_bt = QPushButton('Entrer')
        # self.submit_bt.clicked.connect(self.handle_part_search)
        self.part_status = QLabel()

        self.search_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.search_shortcut.activated.connect(lambda: self.handle_part_search(self.input.text()))

        grid.addWidget(label, 1, 1, 1, 1)
        grid.addWidget(self.input, 1, 2, 1, 1)
        grid.addWidget(self.submit_bt, 1, 3, 1, 1)
        grid.addWidget(self.part_status, 2, 1, 1, 3)

        self.setLayout(grid)

    def get_part(self):
        """
        Returns the part string
        :return:
        """
        return self.input.text()

    def handle_part_search(self, text_input):
        """
        Emits new part selection signal that is received by the inspector
        :return:
        """
        if len(text_input) == 0:
            self.part_status.setText(self.invalid_code)
        elif not PartCatalog.get_part(text_input):
            self.part_selection_signal.emit(text_input)
            self.part_status.setText(self.catalog_absent)
        else:
            self.part_selection_signal.emit(text_input)
            self.part_status.setText(self.catalog_present)


    def update_completer(self):
        completer = QCompleter(PartCatalog.part_list())
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.input.setCompleter(completer)

    def display_blank(self):
        """
        Displays blank value on all input elements
        :return:
        """
        self.input.setText('')
        self.input.setDisabled(True)
        self.submit_bt.setDisabled(True)

    def display_content(self, content: StorageObject):
        """
        Changes the text in lineEdit
        TODO when is completer being updated???
        :param content:
        :return:
        """
        self.input.setDisabled(False)
        self.submit_bt.setDisabled(False)
        self.input.setText(content.part_code)
        # self.input.setCompleter(PartCatalog.part_list())

    def update_information(self, element):
        """
        OLD
        :param element:
        :return:
        """
        if issubclass(type(element), StorageObject):
            print('good update')
            self.input.setText(element.part_code)
            self.update_completer()
        elif not element:       # uselss replaced by display_blank
            self.input.setText('')

