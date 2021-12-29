from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
import sys

class Child(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(50, 50, 75, 75)
        self.create_layout()
        self.resize(50, 100)

    def create_layout(self):
        vbox = QVBoxLayout()

        btn1 = QPushButton('Button 1')
        btn2 = QPushButton('Button 2')
        btn3 = QPushButton('Button 3')

        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        self.setLayout(vbox)




# app = QApplication(sys.argv)
# widget = Child()
# widget.show()
# sys.exit(app.exec())