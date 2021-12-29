from PyQt6.QtWidgets import QWidget, QMainWindow, QMenuBar, QApplication, QMenu, QToolBar, QLabel
import sys
from centralWidget import CentralWidget
from settings import SettingsWindow
from importer import ImporterWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sample window')
        self.setGeometry(50, 50, 1200, 650)
        self.context_window1 = QMainWindow()

        self.create_menus()
        self.create_tool_bar()
        self.create_status_bar()
        self.set_main_content()

    def set_main_content(self):
        widget = CentralWidget()
        widget.setStyleSheet('background-color:blue')
        widget.resize(200, 200)
        self.setCentralWidget(widget)

    def create_menus(self):
        menu_bar = self.menuBar()
        files_menu = menu_bar.addMenu('Files')
        parts_menu = menu_bar.addMenu('Pièces')
        importer = parts_menu.addMenu('importer')
        importer.addAction('piece')

        catalog_menu = menu_bar.addMenu('Catalogue')
        catalog_import = catalog_menu.addAction('importer calatogue')
        catalog_import.triggered.connect(self.show_importer)


        suppliers_menu = menu_bar.addMenu('Fournisseurs')
        settings_menu = menu_bar.addAction('Paramètres')
        settings_menu.triggered.connect(self.show_settings)


    def show_settings(self):
        print('show settings')
        settings_window = SettingsWindow()
        settings_window.open_window(self.context_window1)
        self.context_window1.show()

    def show_importer(self):
        print('show importer')
        importer_window = ImporterWindow()
        importer_window.open_window(self.context_window1)
        self.context_window1.show()


    def create_status_bar(self):
        """
        Boiler plate for status bar
        :return:
        """
        status_bar = self.statusBar()
        status_bar.setStyleSheet('background-color:red')
        label = QLabel('This is a label')
        label2 = QLabel('This is status')
        status_bar.addPermanentWidget(label, stretch=1)
        status_bar.addPermanentWidget(label2, stretch=5)

    def create_tool_bar(self):
        """
        boiler plate for tool bar
        :return:
        """
        test = self.addToolBar('TEST')
        click = test.addAction('hello')
        click.triggered.connect(self.test)


    def test(self):
        print('this is a test')



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()  # inherited from QMainWindow
sys.exit(app.exec())
