import unittest

from CanReader.Exceptions.CanCheck import *


class TestCanCheck(unittest.TestCase):

    def test_id_type(self):
        # Make sure id is a valid type -> integer
        self.assertRaises(TypeError, check_id, "string")
        self.assertRaises(TypeError, check_id, 'a')
        self.assertRaises(TypeError, check_id, 43.5)
        self.assertRaises(TypeError, check_id, True)
        self.assertRaises(TypeError, check_id, None)

        check_id(15)

    def test_group_id_value(self):
        # Make sure group id is in valid range 0 - 999
        self.assertRaises(ValueError, check_group_id, -1)
        self.assertRaises(ValueError, check_group_id, 1000)

        check_group_id(0)
        check_group_id(500)
        check_group_id(999)

    def test_group_id_type(self):
        # Make sure group id is a valid type -> integer
        self.assertRaises(TypeError, check_group_id, "string")
        self.assertRaises(TypeError, check_group_id, 'a')
        self.assertRaises(TypeError, check_group_id, 45.5)
        self.assertRaises(TypeError, check_group_id, True)
        self.assertRaises(TypeError, check_group_id, None)

    def test_widget_id_value(self):
        # Make sure group id is in valid range 0 - 50
        self.assertRaises(ValueError, check_widget_id, -1)
        self.assertRaises(ValueError, check_widget_id, 60)

        check_widget_id(0)
        check_widget_id(10)
        check_widget_id(50)

    def test_widget_id_type(self):
        # Make sure group id is a valid type -> integer
        self.assertRaises(TypeError, check_widget_id, "string")
        self.assertRaises(TypeError, check_widget_id, 'a')
        self.assertRaises(TypeError, check_widget_id, 45.5)
        self.assertRaises(TypeError, check_widget_id, True)
        self.assertRaises(TypeError, check_widget_id, None)

    def test_can_id_value(self):
        # Make sure can id is in Hex string number of max length 8
        self.assertRaises(ValueError, check_can_id, "b000b000a")
        self.assertRaises(ValueError, check_can_id, "")

        check_can_id("603")
        check_can_id("a0500f0f")
        check_can_id("0")
        check_can_id("60")

    def test_can_id_type(self):
        # Make sure can id is a valid type -> integer
        self.assertRaises(TypeError, check_can_id, [50, 10])
        self.assertRaises(TypeError, check_can_id, ["50", "10"])
        self.assertRaises(TypeError, check_can_id, 43.5)
        self.assertRaises(TypeError, check_can_id, -1)
        self.assertRaises(TypeError, check_can_id, True)
        self.assertRaises(TypeError, check_can_id, None)

    def test_name_type(self):
        # Make sure name is a valid type -> string
        self.assertRaises(TypeError, check_name, 666)
        self.assertRaises(TypeError, check_name, 43.5)
        self.assertRaises(TypeError, check_name, -0.5)
        self.assertRaises(TypeError, check_name, True)
        self.assertRaises(TypeError, check_name, None)

        check_name("Name")
        check_name("Name name 00 name ? 00")

    def test_unit_type(self):
        # Make sure unit is a valid type -> string
        self.assertRaises(TypeError, check_unit, 666)
        self.assertRaises(TypeError, check_unit, 43.5)
        self.assertRaises(TypeError, check_unit, -0.5)
        self.assertRaises(TypeError, check_unit, True)
        self.assertRaises(TypeError, check_unit, None)

        check_name("Name")
        check_name("Name name 00 name ? 00")

    def test_start_bit_type(self):
        # Make sure start bit is a valid type -> integer
        self.assertRaises(TypeError, check_start_bit, "string")
        self.assertRaises(TypeError, check_start_bit, 'a')
        self.assertRaises(TypeError, check_start_bit, 43.5)
        self.assertRaises(TypeError, check_start_bit, True)
        self.assertRaises(TypeError, check_start_bit, None)

    def test_start_bit_value(self):
        # Make sure start bit is in valid range 0 - 63
        self.assertRaises(ValueError, check_start_bit, -1)
        self.assertRaises(ValueError, check_start_bit, 64)

        check_start_bit(0)
        check_start_bit(30)
        check_start_bit(63)

    def test_length_type(self):
        # Make sure length is a valid type -> integer
        self.assertRaises(TypeError, check_length, "string")
        self.assertRaises(TypeError, check_length, 'a')
        self.assertRaises(TypeError, check_length, 43.5)
        self.assertRaises(TypeError, check_length, True)
        self.assertRaises(TypeError, check_length, None)

    def test_length_value(self):
        # Make sure length is in valid range 1 - 63
        self.assertRaises(ValueError, check_length, -1)
        self.assertRaises(ValueError, check_length, 0)
        self.assertRaises(ValueError, check_length, 64)

        check_length(1)
        check_length(25)
        check_length(63)

    def test_multiplier_type(self):
        # Make sure multiplier is a valid type -> integer or float
        self.assertRaises(TypeError, check_multiplier, "string")
        self.assertRaises(TypeError, check_multiplier, 'a')
        self.assertRaises(TypeError, check_multiplier, True)
        self.assertRaises(TypeError, check_multiplier, None)

    def test_multiplier_value(self):
        # Make sure multiplier cannot be 0
        self.assertRaises(ValueError, check_multiplier, 0)

        check_multiplier(-1)
        check_multiplier(-10.5)
        check_multiplier(15)
        check_multiplier(0.0225)

    def test_offset_type(self):
        # Make sure multiplier is a valid type -> integer or float
        self.assertRaises(TypeError, check_offset, "string")
        self.assertRaises(TypeError, check_offset, 'a')
        self.assertRaises(TypeError, check_offset, True)
        self.assertRaises(TypeError, check_offset, None)

        check_multiplier(-1)
        check_multiplier(-10.5)
        check_multiplier(15)
        check_multiplier(0.0225)

    def test_endian_type(self):
        # Make sure endian is str
        self.assertRaises(TypeError, check_endian, 666)
        self.assertRaises(TypeError, check_endian, 43.5)
        self.assertRaises(TypeError, check_endian, -0.5)
        self.assertRaises(TypeError, check_endian, True)
        self.assertRaises(TypeError, check_endian, None)

    def test_endian_value(self):
        # Make sure endian is 'L' or 'B'
        self.assertRaises(ValueError, check_endian, "A")
        self.assertRaises(ValueError, check_endian, "l")
        self.assertRaises(ValueError, check_endian, "Aada")
        self.assertRaises(ValueError, check_endian, "-100")

        check_endian("L")
        check_endian("B")

    def test_value_type(self):
        # Make sure value is float or int
        self.assertRaises(TypeError, check_value, "string")
        self.assertRaises(TypeError, check_value, 'a')
        self.assertRaises(TypeError, check_value, True)
        self.assertRaises(TypeError, check_value, None)

        check_value(15)
        check_value(1.5)
        check_value(-15)
        check_value(-1.5)
        check_value(0)

    def test_raw_data_type(self):
        # Make sure raw data are byte array
        self.assertRaises(TypeError, check_raw_data, "mka")
        self.assertRaises(TypeError, check_raw_data, 'a')
        self.assertRaises(TypeError, check_raw_data, -50)
        self.assertRaises(TypeError, check_raw_data, 50)
        self.assertRaises(TypeError, check_raw_data, [0, 50, 20])
        self.assertRaises(TypeError, check_raw_data, 1.5)
        self.assertRaises(TypeError, check_raw_data, False)
        self.assertRaises(TypeError, check_raw_data, None)
        self.assertRaises(TypeError, check_raw_data, "0b0010000101")

    def test_raw_data_length(self):
        # Make sure raw data are 12 bytes long
        self.assertRaises(ValueError, check_raw_data, bytearray([0, 50, 20]))
        self.assertRaises(ValueError, check_raw_data, bytearray([0, 50, 20, 0, 50, 20, 0, 50, 20,0, 50, 20, 0, 50, 20]))

        check_raw_data(bytearray([255, 0, 6, 3, 0, 00, 0, 0, 0, 0, 0, 0]))
