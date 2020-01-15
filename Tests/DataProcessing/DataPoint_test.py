import unittest
from CanReader.DataProcessing.DataPoint import DataPoint

class TestDataPoint(unittest.TestCase):
    """
        Unit test definition for class called DataPoint.
    """

    def test_id_value(self):
        # Make sure id is in valid range 0 - 999
        self.assertRaises(ValueError, DataPoint.check_id, -1)
        self.assertRaises(ValueError, DataPoint.check_id, 1000)

    def test_id_type(self):
        # Make sure id is a valid type -> integer
        self.assertRaises(TypeError, DataPoint.check_id, "string")
        self.assertRaises(TypeError, DataPoint.check_id, 'a')
        self.assertRaises(TypeError, DataPoint.check_id, 43.5)
        self.assertRaises(TypeError, DataPoint.check_id, True)

    def test_group_id_value(self):
        # Make sure group id is in valid range 0 - 999
        self.assertRaises(ValueError, DataPoint.check_group_id, -1)
        self.assertRaises(ValueError, DataPoint.check_group_id, 1000)

    def test_group_id_type(self):
        # Make sure group id is a valid type -> integer
        self.assertRaises(TypeError, DataPoint.check_group_id, "string")
        self.assertRaises(TypeError, DataPoint.check_group_id, 'a')
        self.assertRaises(TypeError, DataPoint.check_group_id, 43.5)
        self.assertRaises(TypeError, DataPoint.check_group_id, True)

    def test_name_type(self):
        # Make sure name is a valid type -> string
        self.assertRaises(TypeError, DataPoint.check_name, 666)
        self.assertRaises(TypeError, DataPoint.check_name, 43.5)
        self.assertRaises(TypeError, DataPoint.check_name, True)

    def test_value_type(self):
        # Make sure multiplier is a valid type -> integer or float
        self.assertRaises(TypeError, DataPoint.check_value, "string")
        self.assertRaises(TypeError, DataPoint.check_value, 'a')
        self.assertRaises(TypeError, DataPoint.check_value, True)



