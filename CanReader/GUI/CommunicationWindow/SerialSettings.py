import logging

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QComboBox, QLineEdit

from CanReader.Communication.SerialCom import SerialCom
from CanReader.Config.Communication.ComConfigHandler import ComConfigHandler
from CanReader.GUI.UpdateWindow.WarningWindow import WarningWindow


class SerialSettingWindow(QMainWindow):
    """
        :Inherit: :class:`QMainWindow`

        :Description:
            Create window with settings for serial communication.\n
            Let user adjust configuration for serial communication.\n
            UI was created in Qt Designer and loaded from "SerialSettings.ui"

        :param parent: Parent widget
        :type parent: QWidget
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
        """
            :Description:
                Loads a show all available COM ports.
        """
        self.cbox_ports.clear()

        port_list = SerialCom.available_com_ports()

        for port in port_list:
            self.cbox_ports.addItem(port)

    def show_actual_port(self):
        """
            :Description:
                Show actual port settings if saved port is available on system.
        """
        if self.port in SerialCom.available_com_ports():
            self.cbox_ports.setCurrentText(self.port)

    def show_actual_baud_rate(self):
        """
            :Description:
                Show actual baud rate setting.
        """
        self.baud_input.setText(str(self.baud_rate))

    def save_settings(self):
        """
            :Description:
                Save new serial configuration.\n
                If error is raised Warning Window will pop up.

            :raises ValueError:
                -- Baud rate in not convertible to integer.\n
                -- Port is empty.

            :raises TypeError:
                Port is not a str.

            :raises ArithmeticError:
                Baud rate is not in range 300 - 921600.

            :raises OSError:
                Port cannot be find on the system.
        """
        port = self.cbox_ports.currentText()
        baud_rate = self.baud_input.text()

        if self.check_baud_rate(baud_rate) and self.check_port(port):
            self.config.update_serial_info(port, baud_rate)
            self.close()

    @staticmethod
    def check_baud_rate(baud_rate):
        """
            :Description:
                Check if baud is convertible int in range of 300 - 921600.\n
                If error is raised Warning Window will pop up.

            :param baud_rate: Baud rate.
            :type baud_rate: int

            :raises ValueError:
                Baud rate in not convertible to integer.

            :raises ArithmeticError:
                Baud rate is not in range 300 - 921600.

            :return: True if check is passed.
            :rtype: bool
        """
        try:
            if not(300 <= int(baud_rate) <= 921600):
                raise ArithmeticError
            return True
        except ValueError:
            WarningWindow.show_warning_window("Baud rate Error", "Baud rate must be an integer")
            logging.info("User tried to input {}. Baud rate must be an integer".format(baud_rate))
            return False
        except ArithmeticError:
            WarningWindow.show_warning_window("Baud rate Error", "Baud rate must be in range 300 - 921600")
            logging.info("User tried to input {}. Baud rate must be in range 300 - 921600".format(baud_rate))
            return False

    @staticmethod
    def check_port(port):
        """
            :Description:
                Check if port is a non empty str and can be found on the system.

            :param port: Com port name.
            :type port: str

            :raises TypeError:
                Port is not a str.

            :raises ValueError:
                Port is empty.

            :raises OSError:
                Port cannot be find on the system.

            :return: True if check is passed.
            :rtype: bool
        """
        try:
            if type(port) != str:
                raise TypeError
            if port == "":
                raise ValueError
            if port.upper() not in SerialCom.available_com_ports():
                raise OSError
            return True
        except ValueError:
            WarningWindow.show_warning_window("Port Error", "Port cannot be empty.")
            logging.info("User tried to empty port. Port must be a system accessible.")
            return False
        except TypeError:
            WarningWindow.show_warning_window("Port Error", "Port must be string.")
            logging.info("User tried to type {}. Port must be string.".format(type(port)))
            return False
        except OSError:
            WarningWindow.show_warning_window("Port Error", "Selected port was not found on the system.")
            logging.info("User tried to input {}. Port must be a system accessible.".format(port))
            return False
