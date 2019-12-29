import unittest
from CanReader.DataProcessing.DataDecoder import DataDecoder

class TestDataDecoder(unittest.TestCase):
    """
        Unit test definition for class called DataDecoder.
    """

    def test_id_type(self):
        # Make sure id is a valid type -> integer
        self.assertRaises(TypeError, DataDecoder.check_id, "string")
        self.assertRaises(TypeError, DataDecoder.check_id, 'a')
        self.assertRaises(TypeError, DataDecoder.check_id, 43.5)
        self.assertRaises(TypeError, DataDecoder.check_id, True)

    def test_id_value(self):
        # Make sure id is in valid range 0, 999
        self.assertRaises(ValueError, DataDecoder.check_id, -1)
        self.assertRaises(ValueError, DataDecoder.check_id, 1000)

    def test_data_type(self):
        # Make sure data are valid type -> binary
        self.assertRaises(TypeError, DataDecoder.check_data, "string")
        self.assertRaises(TypeError, DataDecoder.check_data, 'a')
        self.assertRaises(TypeError, DataDecoder.check_data, 43)
        self.assertRaises(TypeError, DataDecoder.check_data, 43.5)
        self.assertRaises(TypeError, DataDecoder.check_data, True)
        self.assertRaises(TypeError, DataDecoder.check_data, "1111111111111111111111110111100010101010101110111100110011111000")