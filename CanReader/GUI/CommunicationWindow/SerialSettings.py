from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QComboBox, QLineEdit

from Config.Communication.ComConfigHandler import ComConfigHandler
from Communication.SerialCom import SerialCom
from GUI.UpdateWindow.WarningWindow import WarningWindow


class SerialSettingWindow(QMainWindow):
    """
        Take care about settings of serial communication.
    """

    def __init__(self, parent):
        QMainWindow.__init__(self)
        uic.loadUi('GUI/CommunicationWindow/SerialSettings.ui', self)
        self.parent = parent

        # UI interface
        self.button_save = self.findChild(QPushButton, "button_save")
        self.button_save.clicked.connect(self.save_settings)

        self.cbox_ports = self.findChild(QComboBox, "cbox_ports")
        self.baud_input = self.findChild(QLineEdit, "baud_input")

        # Get current settings
        self.config = ComConfigHandler()
        self.port, self.baud_rate = self.config.load_serial_info()

        # Show ports and baud rates
        self.update_available_ports()

        self.show_actual_port()
        self.show_actual_baud_rate()

        self.show()

    def update_available_ports(self):
        self.cbox_ports.clear()

        port_list = SerialCom.available_com_ports()

        for port in port_list:
            self.cbox_ports.addItem(port)

    def show_actual_port(self):
        if self.port in SerialCom.available_com_ports():
            self.cbox_ports.setCurrentText(self.port)

    def show_actual_baud_rate(self):
        self.baud_input.setText(str(self.baud_rate))

    def save_settings(self):
        port = self.cbox_ports.currentText()
        baud_rate = self.baud_input.text()

        if self.check_baud_rate(baud_rate):
            self.config.update_serial_info(port, baud_rate)
            self.close()

    @staticmethod
    def check_baud_rate(baud_rate):
        try:
            if not(300 <= int(baud_rate) <= 921600):
                raise ArithmeticError
            return True
        except ValueError:
            WarningWindow.show_warning_window("Baud rate Error", "Baud rate must be an integer")
        except ArithmeticError:
            WarningWindow.show_warning_window("Baud rate Error", "Baud rate must be in range 300 - 921600")
