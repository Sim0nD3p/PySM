from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt
from backend.PartCatalog import PartCatalog


class ConfirmationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.repo = {}

        self.vbox = QVBoxLayout()

        self.tree = QTreeWidget()
        self.confirm_button = QPushButton('Importer')
        self.vbox.addWidget(self.tree)
        self.vbox.addWidget(self.confirm_button)
        self.setLayout(self.vbox)


    def update_tree(self, list, decoder_instructions):
        """
        Updates the tree filtering present and absent parts to import
        :param list: part's dict data gotten from importer
        :param decoder_instructions: decoder instructions
        :return:
        """
        self.tree.clear()
        self.tree.setColumnCount(2)


        absent = QTreeWidgetItem(['Pièces à ajouter'])
        present = QTreeWidgetItem(['Pièces en conflit'])

        self.tree.setHeaderHidden(True)
        self.tree.setColumnWidth(0, 400)
        self.tree.addTopLevelItem(present)
        self.tree.addTopLevelItem(absent)

        for part in list:
            part_code = part['part/code']
            print(part_code)
            if PartCatalog.check_presence(part_code):
                e = QTreeWidgetItem([part_code, 'remplacer'])
                e.setData(1, 1, part)
                e.setData(1, 2, decoder_instructions)
                present.addChild(e)
                e.setCheckState(1, Qt.CheckState.Checked)
            else:
                e = QTreeWidgetItem([part_code, 'importer'])
                e.setData(1, 1, part)
                e.setData(1, 2, decoder_instructions)
                absent.addChild(e)
                e.setCheckState(1, Qt.CheckState.Checked)

        self.tree.expandAll()
        self.tree.itemChanged.connect(self.handle_selection)

    def handle_selection(self, e):
        print(e.checkState(1))







