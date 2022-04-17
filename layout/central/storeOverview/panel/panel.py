from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Panel(QWidget):
    # signals useless we should directly connect to button signal
    submit_signal = pyqtSignal(name='submit_signal')
    cancel_signal = pyqtSignal(name='cancel_signal')

    def __init__(self):
        super().__init__()
        # base UI
        self.setContentsMargins(5, 5, 5, 5)     # TODO play with it to find perfect UI
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Base)

        # main vbox setup
        self.main_vbox = QVBoxLayout()
        self.main_vbox.setContentsMargins(0, 0, 0, 0)

        self.tool_bar = QToolBar()
        self.main_vbox.addWidget(self.tool_bar)

        self.container_inspector = QWidget()
        self.main_vbox.addWidget(self.container_inspector)

        # buttons setup
        button_hbox = QHBoxLayout()
        self.submit_button = QPushButton('Ok')
        self.cancel_button = QPushButton('Cancel')
        button_hbox.addSpacing(100)
        button_hbox.addWidget(self.cancel_button)
        button_hbox.addWidget(self.submit_button)
        self.main_vbox.addLayout(button_hbox)


        self.setLayout(self.main_vbox)


    def set_tool_bar(self, tool_bar: QToolBar):
        """
        Sets tool bar at the top of the panel
        :param tool_bar:
        :return:
        """
        self.tool_bar = tool_bar
        self.main_vbox.insertWidget(0, self.tool_bar)


    def set_inspector(self, inspector):
        """
        Sets main inspector that operates with backend
        :param inspector:
        :return:
        """
        self.container_inspector = inspector
        self.main_vbox.insertWidget(1, self.container_inspector)


    def show_panel(self, width=250):
        """
        Shows panel by setting minimum and maximum width
        :param width:
        :return: void
        """
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)

    def hide_panel(self):
        """
        Hides panel by setting minimum and maximum width
        :return: void
        """
        self.setMaximumWidth(0)
        self.setMinimumWidth(0)

