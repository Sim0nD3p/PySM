from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from layout.central.storeOverview.panel.rackingCard import RackingCard
from layout.central.storeOverview.physicalViewer.storeOverallTopView import StoreTopVisualizer
from layout.central.storeOverview.physicalViewer.toolBarControls import StoreViewerControls

class StoreOverviewPanel(QWidget):
    def __init__(self, store_viewer: StoreTopVisualizer):
        super().__init__()
        self.setMaximumWidth(500)
        self.main_vbox = QVBoxLayout()




        self.store_viewer_controls = StoreViewerControls(store_viewer=store_viewer)
        self.racking_card = RackingCard()


        self.main_vbox.addWidget(self.store_viewer_controls)
        self.main_vbox.addWidget(self.racking_card)

        # buttons for testing
        hbox = QHBoxLayout()
        but = QPushButton('test1')
        but.clicked.connect(lambda: self.racking_card.update_child_informations('BON MATIN'))
        hbox.addWidget(but)

        self.main_vbox.addLayout(hbox)

        self.setLayout(self.main_vbox)


    def test(self):
        print('winner test')

