from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from backend.PartCatalog import PartCatalog


class FilterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(500, 200)
        self.parent = parent
        self.setStyleSheet('background-color:blue')

        self.text_search = QWidget()
        self.line_edit = QLineEdit()

        self.search_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.search_shortcut.activated.connect(self.submit_search)

        self.b_search = QPushButton('soumettre')
        self.b_search.clicked.connect(self.submit_search)

        self.create_text_search()
        self.create_layout()

    def submit_search(self):
        print('shoudl search')
        text = self.line_edit.text()
        results = PartCatalog.text_search(text)
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



    def create_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.text_search)

        label = QLabel('this is label')
        vbox.addWidget(label)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
