from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QMessageBox

from CanReader.GUI.UpdateWindow.UpdateWindow import UpdateWindow


class MainWindow(QMainWindow):
    """
        Main class of graphical part.
         Contains all other graphical widget and send data to them
    """

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
        """
            This method takes data received from formula and sends them to place where will be displayed
            :param data: list of DataPoints containing decoded and processed data from formula
            :type data: DataPoint
        """
        value1 = data[0].value
        name1 = data[0].name
        value2 = data[1].value
        name2 = data[1].name

        self.label_1_value.setText(str(value1))
        self.label_1_name.setText(name1)
        self.label_2_value.setText(str(value2))
        self.label_2_name.setText(name2)

    def update_can_msg(self, can_msg):
        """
            This method update can message label in gui
            :param can_msg: last received can message
        """
        self.can_msg.setText(str(can_msg))

    def update_status(self, status):
        """
            This method update connection status between app and formula
            :param status: Status can be "Offline" , "Online" , "Connecting"
        """
        self.status.setText(status)

    def open_update_window(self):
        """
            This method is invoked when update button is clicked.
            Open update window, where user can adjust configuration for selected variable
        """
        self.update_win = UpdateWindow(self, 1)


