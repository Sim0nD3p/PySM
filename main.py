from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMenu
import sys
from layout.central.centralWidget import CentralWidget
from layout.settings.settingsLayout import SettingsWindow
from layout.importer.importer import ImporterWindow
from backend.PartCatalog import PartCatalog
from backend.writers.partCatalogWriter import PartCatalogWriter
from backend.loaders.partCatalogLoader import PartCatalogLoader
from backend.writers.storeFloorWriter import *
from backend.storeFloor import *
from backend.loaders.storeFloorLoader import *

from layout.central.storeOverview.storeViewerWidget.actions import MoveUp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.context_window1 = QMainWindow()
        self.setWindowTitle('Sample window')
        self.setGeometry(50, 50, 1000, 600)
        self.part_catalog = PartCatalog()
        self.importer_window = ImporterWindow(self)
        self.importer_window.importer.confirmation_widget.confirm_button.clicked.connect(self.part_catalog_update)

        # self.tool_bar = self.addToolBar()


        self.main_widget = CentralWidget()
        self.setCentralWidget(self.main_widget)

        self.create_menus()
        self.create_tool_bar()
        self.create_status_bar()
        self.backend_startup()


    def create_menus(self):
        menu_bar = self.menuBar()
        files_menu = menu_bar.addMenu('Files')
        # parts_menu = menu_bar.addMenu('Pièces')
        # importer = parts_menu.addMenu('importer')
        # importer.addAction('piece')

        catalog_menu = menu_bar.addMenu('Catalogue')
        catalog_import = catalog_menu.addAction('Importer')
        catalog_import.triggered.connect(self.show_importer)
        catalog_delete = catalog_menu.addAction('Supprimer catalogue')

        def delete_catalog():
            PartCatalog.delete_catalog()
            self.part_catalog_update()

        catalog_delete.triggered.connect(delete_catalog)

        catalog_save = catalog_menu.addMenu('Sauvegarder catalogue')
        save = catalog_save.addAction('Enregistrer')

        save.triggered.connect(PartCatalogWriter.save_default)


        settings_menu = menu_bar.addAction('Paramètres')
        settings_menu.triggered.connect(self.show_settings)

        store_menu = menu_bar.addMenu('Magasin')
        # mu = MoveUp(self)
        def create_store_menu(sm):
            save = sm.addAction('Sauvegarder')
            save.triggered.connect(lambda: StoreFloorWriter().save_default(StoreFloor()))


        create_store_menu(store_menu)






    def backend_startup(self):
        print('initiating app')
        StoreFloorLoader.load_floor_from_xml(file_path='backend/appData/storeFloor.xml')
        PartCatalogLoader.load_xml_catalog('backend/appData/catalog_new.xml')
        self.part_catalog_update()
        # self.main_widget.store_overview.store_visual.paintGL()


    def show_settings(self):
        print('show settings')
        settings_window = SettingsWindow()
        settings_window.open_window(self.context_window1)
        self.context_window1.show()

    def show_importer(self):
        print('show importer')

        self.importer_window.open_window(self.context_window1)
        self.context_window1.show()


    def handle_part_import(self, list):
        print('this is main')
        for part in list:
            self.part_catalog.add_part(part)

        self.main_widget.catalog_overview.list_widget.draw_list(list)


    def part_catalog_update(self):
        """
        Function to run when new catalog update to update UI
        :return:
        """
        self.main_widget.catalog_overview.update_catalog_overview_features()



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

        def test():
            print('test')

        widget = QWidget()
        vbox = QVBoxLayout()
        var = 'test'
        index = self.main_widget.stackedlayout.currentIndex()
        change_up = QPushButton('+')
        change_up.clicked.connect(lambda: self.main_widget.handle_stack_change('up'))
        change_down = QPushButton('-')
        change_down.clicked.connect(lambda: self.main_widget.handle_stack_change('down'))




        vbox.addWidget(change_up)
        vbox.addWidget(change_down)

        widget.setLayout(vbox)


        test = self.addToolBar('test')
        test.addWidget(widget)
        click = test.addAction('hello')
        click.triggered.connect(self.test)


    def test(self):
        print('this is a test')



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()  # inherited from QMainWindow
sys.exit(app.exec())
