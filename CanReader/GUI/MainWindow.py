from PyQt5 import uic, QtWidgets, QtCore

from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QApplication, \
    QLabel
from CanReader.GUI.UpdateWindow.UpdateWindow import UpdateWindow


class MainWindow(QMainWindow):

    update_config_signal = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('CanReader/GUI/MainWindow.ui', self)

        self.can_msg = self.findChild(QLabel, "label_can_msg")
        self.status = self.findChild(QLabel, "label_status")

        self.button_update = self.findChild(QPushButton, "button_update")
        self.button_update.clicked.connect(self.open_update_window)

        self.label_1_name = self.findChild(QLabel, "label")
        self.label_1_value = self.findChild(QLabel, "label_3")
        self.label_2_name = self.findChild(QLabel, "label_6")
        self.label_2_value = self.findChild(QLabel, "label_5")

        self.show()

    def update_labels(self, data):
        value1 = data[0].value
        name1 = data[0].name
        value2 = data[1].value
        name2 = data[1].name

        self.label_1_value.setText(str(value1))
        self.label_1_name.setText(name1)
        self.label_2_value.setText(str(value2))
        self.label_2_name.setText(name2)

    def update_can_msg(self, can_msg):
        self.can_msg.setText(str(can_msg))

    def update_status(self, status):
        self.status.setText(status)

    def open_update_window(self):
        self.update_win = UpdateWindow(self, 1)


