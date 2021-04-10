import logging
import socket

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit

from CanReader.Config.Communication.ComConfigHandler import ComConfigHandler
from CanReader.GUI.UpdateWindow.WarningWindow import WarningWindow


class WifiSettingWindow(QMainWindow):
    """
        :Inherit: :class:`QMainWindow`

        :Description:
            Create window with settings for Wi-Fi communication.\n
            Let user adjust configuration for Wi-Fi communication.\n
            UI was created in Qt Designer and loaded from "WifiSettings.ui"

        :param parent: Parent widget
        :type parent: QWidget
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
        """
            :Description:
                Show actual ip settings.
        """
        self.ip_input.setText(str(self.ip))

    def show_actual_port(self):
        """
            :Description:
                Show actual port settings .
        """
        self.port_input.setText(str(self.port))

    def save_settings(self):
        """
            :Description:
                Save new Wi-Fi configuration.

            :raises ValueError:
                -- Port in not convertible to integer.\n

            :raises ArithmeticError:
                Port is not in range 1 - 65535.

            :raises OSError:
                IP address is not valid.
        """
        ip = self.ip_input.text()
        port = self.port_input.text()

        if self.check_ip(ip) and self.check_port(port):
            self.config.update_wifi_info(ip, port)
            self.close()

    @staticmethod
    def check_ip(ip):
        """
            :Description:
                Check if IP address is in a valid format.\n
                If error is raised Warning Window will pop up.

            :param ip: IP address.
            :type ip: str

            :raises OSError:
                IP address is not in a valid format.

            :return: True if check is passed.
            :rtype: bool
        """
        try:
            socket.inet_aton(ip)
            return True
        except OSError:
            WarningWindow.show_warning_window("IP Address Error", "IP address is not in valid format.")
            logging.info("User tried to input {}. IP address is not in valid format.".format(ip))
            return False

    @staticmethod
    def check_port(port):
        """
            :Description:
                Check if port is int in range 1 - 65535.\n
                If error is raised Warning Window will pop up.

            :param port: Communication port.
            :type port: int

            :raises ValueError:
                -- Port in not convertible to integer.\n

            :raises ArithmeticError:
                Port is not in range 1 - 65535.

            :return: True if check is passed.
            :rtype: bool
        """
        try:
            if not(1 <= int(port) <= 65535):
                raise ArithmeticError
            return True
        except ArithmeticError:
            WarningWindow.show_warning_window("Port Error", "Port number must be in range 1 - 65535.")
            logging.info("User tried to input {}. Port number must be in range 1 - 65535.".format(port))
            return False
        except ValueError:
            WarningWindow.show_warning_window("Port Error", "Port must be an integer")
            logging.info("User tried to input {}. Port must be an integer".format(port))
            return False
