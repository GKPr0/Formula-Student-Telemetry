import unittest
from CanReader.GUI.UpdateWindow.UpdateWindow import UpdateWindow

class TestDataPoint(unittest.TestCase):
    """
        Unit test definition for class called DataPoint.
    """

    def test_id_value(self):
        # Make sure id is in valid range 0 - 999
        self.assertRaises(ValueError, UpdateWindow.check_config_id, 1000)
        self.assertRaises(ValueError, UpdateWindow.check_config_id, -1)

    def test_id_type(self):
        # Make sure id is integer
        self.assertRaises(TypeError, UpdateWindow.check_config_id, True)
        self.assertRaises(TypeError, UpdateWindow.check_config_id, 15.6)
        self.assertRaises(TypeError, UpdateWindow.check_config_id, "String")
        self.assertRaises(TypeError, UpdateWindow.check_config_id, 'a')




