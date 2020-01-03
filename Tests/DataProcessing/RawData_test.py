import unittest
from CanReader.DataProcessing.RawData import RawData

class TestRawData(unittest.TestCase):
    """
    Unit test definition for class called RawData.
    """

    def test_split_data(self):
        # Make sure function split data gives correct output ID and data
        raw_data = RawData("ID100XFFFFFF78AABBCCF8")

        self.assertEqual(raw_data.split_data(), (100, "0b1111111111111111111111110111100010101010101110111100110011111000"))

    def test_raw_data_type(self):
        # Make sure raw data are string
        self.assertRaises(TypeError, RawData.check_raw_data, -143)
        self.assertRaises(TypeError, RawData.check_raw_data, 666)
        self.assertRaises(TypeError, RawData.check_raw_data, 54.5)
        self.assertRaises(TypeError, RawData.check_raw_data, True)


