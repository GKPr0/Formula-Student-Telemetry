import unittest

from CanReader.Communication.SocketClient import SocketClient


class TestSocketClient(unittest.TestCase):

    def test_check_address(self):
        # Make sure IP address is in valid format -> xxx.xxx.xxx.xxx , xxx -> (0 - 255)
        self.assertRaises(OSError, SocketClient.check_address, "198.162.1.300")
        self.assertRaises(OSError, SocketClient.check_address, "198.162.1001.150")
        self.assertRaises(OSError, SocketClient.check_address, "198.162.001.ff")
        self.assertRaises(OSError, SocketClient.check_address, "198.162.001.150.255")

        SocketClient.check_address("198.162.001")
        SocketClient.check_address("198.162.0.12")
        SocketClient.check_address("198.162.0.255")
        SocketClient.check_address("198")

    def test_check_port_type(self):
        # Make sure port is int
        self.assertRaises(TypeError, SocketClient.check_port, "198.162.1.300")
        self.assertRaises(TypeError, SocketClient.check_port, 52.3)
        self.assertRaises(TypeError, SocketClient.check_port, True)
        self.assertRaises(TypeError, SocketClient.check_port, None)
        self.assertRaises(TypeError, SocketClient.check_port, [15, 16])
        self.assertRaises(TypeError, SocketClient.check_port, '52.3')

    def test_check_port_value(self):
        # Make sure port is in range 1- 65536
        self.assertRaises(ValueError, SocketClient.check_port, -15)
        self.assertRaises(ValueError, SocketClient.check_port, 0)
        self.assertRaises(ValueError, SocketClient.check_port, 165468)
        self.assertRaises(ValueError, SocketClient.check_port, 2**16)

        SocketClient.check_port(1)
        SocketClient.check_port(15645)
        SocketClient.check_port(65535)
