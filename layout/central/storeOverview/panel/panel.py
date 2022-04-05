from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class Panel(QWidget):
    submit_signal = pyqtSignal(name='submit_signal')
    cancel_signal = pyqtSignal(name='cancel_signal')

    def __init__(self):
        super().__init__()
        self.element = None

