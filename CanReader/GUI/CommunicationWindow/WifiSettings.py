import socket

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit

from Config.Communication.ComConfigHandler import ComConfigHandler
from GUI.UpdateWindow.WarningWindow import WarningWindow


class WifiSettingWindow(QMainWindow):
    """
        Take care about settings of wifi communication.
    """

    def __init__(self, parent):
        QMainWindow.__init__(self)
        uic.loadUi('GUI/CommunicationWindow/WifiSettings.ui', self)
        self.parent = parent

        # UI interface
        self.button_save = self.findChild(QPushButton, "button_save")
        self.button_save.clicked.connect(self.save_settings)

        self.ip_input = self.findChild(QLineEdit, "ip_input")
        self.port_input = self.findChild(QLineEdit, "port_input")

        # Get current settings
        self.config = ComConfigHandler()
        self.ip, self.port = self.config.load_wifi_info()

        # Show ip and port
        self.show_actual_port()
        self.show_actual_ip()

        self.show()

    def show_actual_ip(self):
        self.ip_input.setText(str(self.ip))

    def show_actual_port(self):
        self.port_input.setText(str(self.port))

    def save_settings(self):
        ip = self.ip_input.text()
        port = self.port_input.text()

        if self.check_ip(ip) and self.check_port(port):
            self.config.update_wifi_info(ip, port)
            self.close()

    @staticmethod
    def check_ip(ip):
        try:
            socket.inet_aton(ip)
            return True
        except OSError:
            WarningWindow.show_warning_window("IP Address Error", "IP address is not in valid format.")

    @staticmethod
    def check_port(port):
        try:
            if not(1 <= int(port) <= 65535):
                raise ArithmeticError
            return True
        except ArithmeticError:
            WarningWindow.show_warning_window("Port Error", "Port number must be in range 1 - 65535.")
        except ValueError:
            WarningWindow.show_warning_window("Port Error", "Port must be an integer")
