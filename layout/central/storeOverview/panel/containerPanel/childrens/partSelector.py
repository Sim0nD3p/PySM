import PyQt6.QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from backend.PartCatalog import*
from elements.part.Part import *


class PartSelector(QWidget):
    part_selection_signal = pyqtSignal(Part, name='part_selection')

    def __init__(self):
        super().__init__()
        self.completer = QCompleter(PartCatalog.part_list())
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Pièce')
        self.input = QLineEdit()

        self.input.setCompleter(self.completer)
        self.submit_bt = QPushButton('Entrer')
        self.submit_bt.clicked.connect(self.handle_part_search)

        self.search_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.search_shortcut.activated.connect(self.handle_part_search)

        hbox.addWidget(label)
        hbox.addWidget(self.input)
        hbox.addWidget(self.submit_bt)

        self.setLayout(hbox)

    def handle_part_search(self):
        """
        Emits new part selection signal that is received by the inspector
        :return:
        """
        part = PartCatalog.get_part(self.input.text())
        if part:
            self.part_selection_signal.emit(part)
        else:
            print('error part not found in catalog')

    def update_completer(self):
        completer = QCompleter(PartCatalog.part_list())
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.input.setCompleter(completer)