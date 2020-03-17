import unittest
from CanReader.Communication.SocketClient import SocketClient

class TestSocketClient(unittest.TestCase):
    """
    Unit test definition for class called SocketClient.
    """

    def test_ip(self):
        # Make sure given IP address is valid
        self.assertRaises(OSError, SocketClient.check_address, "Afd.168.100.1")
        self.assertRaises(OSError, SocketClient.check_address, "string")
        self.assertRaises(OSError, SocketClient.check_address, "192.168.100.1.2.2")
        self.assertRaises(OSError, SocketClient.check_address, "-192.168.100.1.")

    def test_port_value(self):
        # Make sure port number is in range of 1 - 65536
        self.assertRaises(ValueError, SocketClient.check_port, 0)
        self.assertRaises(ValueError, SocketClient.check_port, -564)
        self.assertRaises(ValueError, SocketClient.check_port, 648292)


    def test_port_type(self):
        # Make sure port number is integer
        self.assertRaises(TypeError, SocketClient.check_port, "String")
        self.assertRaises(TypeError, SocketClient.check_port, 'a')
        self.assertRaises(TypeError, SocketClient.check_port, 54.5)
        self.assertRaises(TypeError, SocketClient.check_port, True)


