import sys
from PyQt6.QtCore import Qt
from PyQt6 import QtOpenGLWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QHBoxLayout, QStylePainter
from PyQt6.QtGui import QPainter, QColor

class Test(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        print('initialize GL')

    def paintGL(self):
        print('paintGL')
        col = QColor(0, 0, 0)
        col.setNamedColor('#ffffff')
        painter = QPainter(self)
        painter.setPen(col)
        painter.drawRect(10, 10, 50, 50)



def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 500, 500)
    widget = Test()
    window.setCentralWidget(widget)
    window.show()
    sys.exit(app.exec())

main()
