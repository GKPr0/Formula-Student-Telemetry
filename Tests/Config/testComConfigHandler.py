import unittest

from CanReader.Config.Communication.ComConfigHandler import ComConfigHandler
from CanReader.Communication.SerialCom import SerialCom
from CanReader.Communication.SocketClient import SocketClient


class TestComConfigHandler(unittest.TestCase):

    def test_load_serial_info(self):
        # Make sure serial info is loadable and in correct format
        com_config = ComConfigHandler()

        port, baud_rate = com_config.load_serial_info()

        self.assertIsNotNone(port)
        self.assertIsNotNone(baud_rate)

        SerialCom.check_baud_rate(baud_rate)

    def test_load_wifi_info(self):
        # Make sure wifi info is loaded and in correct format
        com_config = ComConfigHandler()

        ip, port = com_config.load_wifi_info()

        self.assertIsNotNone(ip)
        self.assertIsNotNone(port)

        SocketClient.check_address(ip)
        SocketClient.check_port(port)
