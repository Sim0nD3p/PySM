from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from layout.central.storeOverview.panel.elementInspector import ElementInspector
from layout.central.storeOverview.physicalViewer.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.physicalViewer.toolBarControls import StoreViewerControls

class StoreOverviewPanel(QWidget):
    def __init__(self, store_viewer: StoreTopVisualizer):
        super().__init__()
        self.setMaximumWidth(500)
        self.main_vbox = QVBoxLayout()
        self.sv = store_viewer




        self.store_viewer_controls = StoreViewerControls(store_viewer=store_viewer)
        self.element_inspector = ElementInspector()


        self.main_vbox.addWidget(self.store_viewer_controls)
        self.main_vbox.addWidget(self.element_inspector)

        # buttons for testing
        hbox = QHBoxLayout()
        but = QPushButton('test1')
        but.clicked.connect(self.sv.draw_shape)
        hbox.addWidget(but)

        self.main_vbox.addLayout(hbox)

        self.setLayout(self.main_vbox)


    def test(self):
        print('winner test')

