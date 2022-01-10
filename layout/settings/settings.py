import sys

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, \
    QStackedLayout, QLineEdit
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtWidgets import QApplication
from layout.settings.widgets.partModel.partModelWidget import PartModelWidget
from layout.settings.widgets.catalog.catalogWidget import CatalogWidget


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setGeometry(100, 100, 500, 500)


    def open_window(self, window):

        settings = Settings()
        window.setCentralWidget(settings)
        window.setGeometry(200, 100, 900, 500)
        window.setWindowTitle('Settings')



class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.categories = ['Général', 'Modèle des pièces', 'Catalogue', 'Magasin']
        # self.setGeometry(50, 50, 200, 200)
        self.glo = 0
        self.part_model_widget = PartModelWidget()
        self.catalog_widget = CatalogWidget()
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
        self.stackedLayout.addWidget(self.catalog_widget)
        self.stackedLayout.addWidget(wid4)


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

