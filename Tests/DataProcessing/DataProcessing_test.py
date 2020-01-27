import unittest
from CanReader.DataProcessing.DataProcessing import DataProcessing
from CanReader.Config.Config import DataConfig
from CanReader.DataProcessing.RawData import RawData

class TestDataProcessing(unittest.TestCase):
    """
        Unit test definition for class called DataProcessing.
    """

    def test_data_process_method(self):
        """
            Test method data_process()
        """
        data_esp = "ID100X111178AABBCCF8"
        raw_data = RawData(data_esp)
        can_id, can_data = raw_data.split_data()
        config = DataConfig(1, 1, "teplota_vody", "Km/hod", 100, 0, 16, 0.005, -100)

        self.assertAlmostEqual(DataProcessing.data_process(can_data, config), 74.775)

    def test_data_decode_method(self):
        """
            Test main class functionality
        """
        data_config_list = []
        data_esp = "ID100XAB000800B00C00"
        raw_data = RawData(data_esp)
        can_id, can_data = raw_data.split_data()
        data_config_list.append(DataConfig(1, 1, "teplota_vody", "Km/hod", 100, 0, 16, 0.005, -100))

        data_processing = DataProcessing(can_id, can_data, data_config_list)
        data_point_list = data_processing.data_decode()

        self.assertAlmostEqual(data_point_list[0].value, 118.88)

    def test_id_type(self):
        # Make sure id is a valid type -> integer
        self.assertRaises(TypeError, DataProcessing.check_id, "string")
        self.assertRaises(TypeError, DataProcessing.check_id, 'a')
        self.assertRaises(TypeError, DataProcessing.check_id, 43.5)
        self.assertRaises(TypeError, DataProcessing.check_id, True)

    def test_id_value(self):
        # Make sure id is in valid range 0, 999
        self.assertRaises(ValueError, DataProcessing.check_id, -1)
        self.assertRaises(ValueError, DataProcessing.check_id, 1000)

    def test_data_type(self):
        # Make sure data are valid type -> binary
        self.assertRaises(TypeError, DataProcessing.check_data, "string")
        self.assertRaises(TypeError, DataProcessing.check_data, 'a')
        self.assertRaises(TypeError, DataProcessing.check_data, 43)
        self.assertRaises(TypeError, DataProcessing.check_data, 43.5)
        self.assertRaises(TypeError, DataProcessing.check_data, True)
        self.assertRaises(TypeError, DataProcessing.check_data, "1111111111111111111111110111100010101010101110111100110011111000")