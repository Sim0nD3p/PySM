from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from backend.PartCatalog import PartCatalog


class ConfirmationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.repo = {}

        self.vbox = QVBoxLayout()

        self.list_widget = QListWidget()
        self.confirm_button = QPushButton('Importer')
        self.confirm_button.clicked.connect(self.import_data)
        self.vbox.addWidget(self.list_widget)
        self.vbox.addWidget(self.confirm_button)
        self.setLayout(self.vbox)

    def handle_click(self, e):
        print(self.repo[e.text()])

    def import_data(self):
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).checkState() == Qt.CheckState.Checked:
                part = self.repo[self.list_widget.item(i).text()]
                PartCatalog.add_part(part)

        print('import data')
        self.parent.main_update()


    def display_import_list(self, import_list):
        self.list_widget.clear()
        print(len(import_list))
        for child in import_list:
            if hasattr(child, 'code'):
                new_item = QListWidgetItem(child.code)
                self.repo[child.code] = child
                if PartCatalog.check_presence(child) == False:
                    new_item.setCheckState(Qt.CheckState.Checked)
                else:
                    new_item.setCheckState(Qt.CheckState.Unchecked)
                self.list_widget.addItem(new_item)
        self.list_widget.itemClicked.connect(self.handle_click)





