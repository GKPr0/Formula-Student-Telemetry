import unittest

from CanReader.Communication.SerialCom import SerialCom


class TestSertialCom(unittest.TestCase):

    def test_check_baud_rate_type(self):
        # Make sure baud rate is int
        self.assertRaises(TypeError, SerialCom.check_baud_rate, "Aaa")
        self.assertRaises(TypeError, SerialCom.check_baud_rate, 9.5)
        self.assertRaises(TypeError, SerialCom.check_baud_rate, 'a')
        self.assertRaises(TypeError, SerialCom.check_baud_rate, [12, 16])
        self.assertRaises(TypeError, SerialCom.check_baud_rate, True)
        self.assertRaises(TypeError, SerialCom.check_baud_rate, None)

    def test_check_baud_rate_value(self):
        # Make sure baud rate is in range 300 - 921600
        self.assertRaises(ValueError, SerialCom.check_baud_rate, 100)
        self.assertRaises(ValueError, SerialCom.check_baud_rate, -10)
        self.assertRaises(ValueError, SerialCom.check_baud_rate, 0)
        self.assertRaises(ValueError, SerialCom.check_baud_rate, 1000000)

        SerialCom.check_baud_rate(300)
        SerialCom.check_baud_rate(15684)
        SerialCom.check_baud_rate(921600)

    def test_check_com_port_type(self):
        # Make sure com port is str
        self.assertRaises(TypeError, SerialCom.check_com_port, 15)
        self.assertRaises(TypeError, SerialCom.check_com_port, 9.5)
        self.assertRaises(TypeError, SerialCom.check_com_port, [12, 16])
        self.assertRaises(TypeError, SerialCom.check_com_port, True)
        self.assertRaises(TypeError, SerialCom.check_com_port, None)

    def test_check_com_port(self):
        # Make sure input port does exists
        self.assertRaises(OSError, SerialCom.check_com_port, "Com11")
        self.assertRaises(OSError, SerialCom.check_com_port, "COM10")

        ports = SerialCom.available_com_ports()

        for port in ports:
            SerialCom.check_com_port(port)
