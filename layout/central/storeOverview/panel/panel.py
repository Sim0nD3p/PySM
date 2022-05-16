from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Panel(QWidget):
    # signals useless we should directly connect to button signal
    submit_signal = pyqtSignal(name='submit_signal')
    cancel_signal = pyqtSignal(name='cancel_signal')
    delete_signal = pyqtSignal(name='delete_signal')

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
        self.buttonsVisible = True

        self.button_hbox = QHBoxLayout()
        self.submit_button = QPushButton('Ok')
        self.submit_button.setMaximumWidth(75)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setMaximumWidth(75)
        self.delete_button = QPushButton('Supprimer')
        self.delete_button.setMaximumWidth(85)
        self.delete_button.setDisabled(True)  # delete disabled by default (should enable)
        self.button_hbox.addSpacing(50)
        self.button_hbox.addWidget(self.delete_button)
        self.button_hbox.addWidget(self.cancel_button)
        self.button_hbox.addWidget(self.submit_button)
        self.main_vbox.addLayout(self.button_hbox)



        self.setLayout(self.main_vbox)

    def enable_buttons(self):
        """
        Enables all bottom buttons
        :return:
        """
        self.delete_button.setDisabled(False)
        self.cancel_button.setDisabled(False)
        self.submit_button.setDisabled(False)

    def disable_buttons(self):
        """
        Enables all bottom buttons
        :return:
        """
        self.delete_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.submit_button.setDisabled(True)




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

