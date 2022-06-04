from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class ColorSelector(QColorDialog):
    def __init__(self):
        super().__init__()
