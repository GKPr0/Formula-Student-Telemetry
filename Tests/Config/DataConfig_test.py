import unittest
from CanReader.Config.DataConfig import DataConfig

class TestDataConfig(unittest.TestCase):
    """
        Unit test definition for class called DataConfig.
    """

    def test_id_value(self):
        # Make sure id is in valid range 0 - 999
        self.assertRaises(ValueError, DataConfig.check_id, -1)
        self.assertRaises(ValueError, DataConfig.check_id, 1000)
        
    def test_id_type(self):
        # Make sure id is a valid type -> integer
        self.assertRaises(TypeError, DataConfig.check_id, "string")
        self.assertRaises(TypeError, DataConfig.check_id, 'a')
        self.assertRaises(TypeError, DataConfig.check_id, 43.5)
        self.assertRaises(TypeError, DataConfig.check_id, True)

    def test_group_id_value(self):
        # Make sure group id is in valid range 0 - 10
        self.assertRaises(ValueError, DataConfig.check_group_id, -1)
        self.assertRaises(ValueError, DataConfig.check_group_id, 15)

    def test_group_id_type(self):
        # Make sure group id is a valid type -> integer
        self.assertRaises(TypeError, DataConfig.check_group_id, "string")
        self.assertRaises(TypeError, DataConfig.check_group_id, 'a')
        self.assertRaises(TypeError, DataConfig.check_group_id, 45.5)
        self.assertRaises(TypeError, DataConfig.check_group_id, True)

    def test_widget_id_value(self):
        # Make sure group id is in valid range 0 - 10
        self.assertRaises(ValueError, DataConfig.check_widget_id, -1)
        self.assertRaises(ValueError, DataConfig.check_widget_id, 15)

    def test_widget_id_type(self):
        # Make sure group id is a valid type -> integer
        self.assertRaises(TypeError, DataConfig.check_widget_id, "string")
        self.assertRaises(TypeError, DataConfig.check_widget_id, 'a')
        self.assertRaises(TypeError, DataConfig.check_widget_id, 45.5)
        self.assertRaises(TypeError, DataConfig.check_widget_id, True)

    def test_can_id_value(self):
        # Make sure can id is in valid range 0 - 999
        self.assertRaises(ValueError, DataConfig.check_can_id, -1)
        self.assertRaises(ValueError, DataConfig.check_can_id, 1000)

    def test_can_id_type(self):
        # Make sure can id is a valid type -> integer
        self.assertRaises(TypeError, DataConfig.check_can_id, "string")
        self.assertRaises(TypeError, DataConfig.check_can_id, 'a')
        self.assertRaises(TypeError, DataConfig.check_can_id, 43.5)
        self.assertRaises(TypeError, DataConfig.check_can_id, True)

    def test_name_type(self):
        # Make sure name is a valid type -> string
        self.assertRaises(TypeError, DataConfig.check_name, 666)
        self.assertRaises(TypeError, DataConfig.check_name, 43.5)
        self.assertRaises(TypeError, DataConfig.check_name, True)

    def test_unit_type(self):
        # Make sure unit is a valid type -> string
        self.assertRaises(TypeError, DataConfig.check_unit, 666)
        self.assertRaises(TypeError, DataConfig.check_unit, 43.5)
        self.assertRaises(TypeError, DataConfig.check_unit, True)

    def test_start_bit_type(self):
        # Make sure start bit is a valid type -> integer
        self.assertRaises(TypeError, DataConfig.check_start_bit, "string")
        self.assertRaises(TypeError, DataConfig.check_start_bit, 'a')
        self.assertRaises(TypeError, DataConfig.check_start_bit, 43.5)
        self.assertRaises(TypeError, DataConfig.check_start_bit, True)

    def test_start_bit_value(self):
        # Make sure start bit is in valid range 0 - 63
        self.assertRaises(ValueError, DataConfig.check_start_bit, -1)
        self.assertRaises(ValueError, DataConfig.check_start_bit, 64)

    def test_length_type(self):
        # Make sure length is a valid type -> integer
        self.assertRaises(TypeError, DataConfig.check_length, "string")
        self.assertRaises(TypeError, DataConfig.check_length, 'a')
        self.assertRaises(TypeError, DataConfig.check_length, 43.5)
        self.assertRaises(TypeError, DataConfig.check_length, True)

    def test_length_value(self):
        # Make sure length is in valid range 1 - 63
        self.assertRaises(ValueError, DataConfig.check_length, -1)
        self.assertRaises(ValueError, DataConfig.check_length, 0)
        self.assertRaises(ValueError, DataConfig.check_length, 64)

    def test_multiplier_type(self):
        # Make sure multiplier is a valid type -> integer or float
        self.assertRaises(TypeError, DataConfig.check_multiplier, "string")
        self.assertRaises(TypeError, DataConfig.check_multiplier, 'a')
        self.assertRaises(TypeError, DataConfig.check_multiplier, True)

    def test_multiplier_value(self):
        # Make sure multiplier is in valid range -> <0,inf)
        self.assertRaises(ValueError, DataConfig.check_multiplier, 0)
        self.assertRaises(ValueError, DataConfig.check_multiplier, -1)
        self.assertRaises(ValueError, DataConfig.check_multiplier, -5.5)

    def test_offset_type(self):
        # Make sure multiplier is a valid type -> integer or float
        self.assertRaises(TypeError, DataConfig.check_offset, "string")
        self.assertRaises(TypeError, DataConfig.check_offset, 'a')
        self.assertRaises(TypeError, DataConfig.check_offset, True)