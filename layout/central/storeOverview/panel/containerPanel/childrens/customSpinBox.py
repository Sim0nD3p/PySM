from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class SpinBox(QSpinBox):
    clicked_signal = pyqtSignal(name='clicked')
    def __init__(self):
        super().__init__()
        self.valueChanged.connect(self.handle_value_change)


    def handle_value_change(self, value):
        print(value)


    def mousePressEvent(self, e: QMouseEvent):
        print('mouse pressed')
        # self.clicked_signal.emit()

