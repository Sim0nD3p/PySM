from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog

class FileSelector(QWidget):
    def __init__(self, parent=None, file_types=None):
        super().__init__()
        self.parent = parent

        self.file_types = file_types


        self.dropdown = QComboBox()
        self.type_selection = QHBoxLayout()
        self.create_type_selection()
        self.create_layout()

    def create_type_selection(self):
        label = QLabel('Type de fichier')
        self.dropdown.addItems(self.file_types)
        self.dropdown.currentIndexChanged.connect(self.parent.handle_filetype_change)
        self.type_selection.addWidget(label)
        self.type_selection.addWidget(self.dropdown)



    def create_layout(self):
        vbox = QVBoxLayout()

        vbox.addLayout(self.type_selection)


        self.setLayout(vbox)