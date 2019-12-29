import unittest
from CanReader.Comunication.SocektServer import SocketServer

class TestSocketServer(unittest.TestCase):
    """
    Unit test definition for class called SocketServer.
    """

    def test_ip(self):
        # Make sure given IP address is valid
        self.assertRaises(OSError, SocketServer.check_address, "Afd.168.100.1")
        self.assertRaises(OSError, SocketServer.check_address, "string")
        self.assertRaises(OSError, SocketServer.check_address, "192.168.100.1.2.2")
        self.assertRaises(OSError, SocketServer.check_address, "-192.168.100.1.")

    def test_port_value(self):
        # Make sure port number is in range of 1 - 65535
        self.assertRaises(ValueError, SocketServer.check_port, 0)
        self.assertRaises(ValueError, SocketServer.check_port, -564)
        self.assertRaises(ValueError, SocketServer.check_port, 648292)


    def test_port_type(self):
        # Make sure port number is integer
        self.assertRaises(TypeError, SocketServer.check_port, "String")
        self.assertRaises(TypeError, SocketServer.check_port, 'a')
        self.assertRaises(TypeError, SocketServer.check_port, 54.5)
        self.assertRaises(TypeError, SocketServer.check_port, True)


