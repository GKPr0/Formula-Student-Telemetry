import unittest
from CanReader.DataProcessing.RawData import RawData

class TestRawData(unittest.TestCase):
    """
    Unit test definition for class called RawData.
    """

    def test_raw_data_type(self):
        # Make sure raw data are string
        self.assertRaises(TypeError, RawData.check_raw_data, -143)
        self.assertRaises(TypeError, RawData.check_raw_data, 666)
        self.assertRaises(TypeError, RawData.check_raw_data, 54.5)
        self.assertRaises(TypeError, RawData.check_raw_data, True)


