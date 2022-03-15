from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt


class RackingProperties(QWidget):
    def __init__(self):
        super().__init__()
        self.racking = None
        self.main_vbox = QVBoxLayout()
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setBackgroundRole(QPalette.ColorRole.Base)

        # TITLE
        title = QLabel('Propriétés')
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        title.setMaximumHeight(25)
        self.main_vbox.addWidget(title)

        # NAME
        self.name_label = QLabel('Nom')
        self.name_le = QLineEdit()
        self.name_le.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(self.name_label)
        name_hbox.addWidget(self.name_le)
        self.main_vbox.addLayout(name_hbox)

        # BUTTON
        but = QLabel('button')
        self.main_vbox.addWidget(but)



        self.create_layout()

    def update_informations(self, racking):
        self.racking = racking
        self.name_label.setText(self.racking)

    def create_layout(self):
        self.main_vbox.setStretch(0, 10)
        self.main_vbox.setStretch(1, 30)
        self.main_vbox.setStretch(2, 10)
        self.setLayout(self.main_vbox)
