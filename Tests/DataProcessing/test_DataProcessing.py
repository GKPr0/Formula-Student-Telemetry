import unittest

from CanReader.DataProcessing.DataProcessing import DataProcessing
from CanReader.Config.CanBus.CanDataConfig import CanDataConfig


class TestDataProcessing(unittest.TestCase):

    def test_data_process(self):

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 16, 1, 100, "B")
        bin_data = "0000000011111111000000001111111100000000111111110000000011111111"

        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(355.0, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 16, 0.5, 0, "B")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(255/2, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 16, 0.25, -100, "B")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual((255/4)-100, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 16, 0.5, 0, "L")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(65280/2, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 8, 16, 1, 0, "L")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(255, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 63, 1, 1, 0, "L")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(1, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 7, 1, 0, "L")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(0, result, 1)

        config = CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 7, 1, 0, "B")
        result = DataProcessing.data_process(bin_data, config)
        self.assertAlmostEqual(0, result, 1)

    def test_data_decode(self):

        can_id = "603"
        can_data = "0000000011111111000000001111111100000000111111110000000011111111"

        config_list = [CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 16, 0.5, 0, "B"),
                       CanDataConfig(2, 2, 2, 2, "Oil temperature", "°C", "603", 16, 16, 0.25, 0, "B"),
                       CanDataConfig(2, 2, 2, 2, "Speed", "km/hod", "600", 0, 16, 1, 0, "B")]

        results = [255/2, 255/4]

        data_processor = DataProcessing(can_id, can_data, config_list)

        data_points = data_processor.data_decode()

        self.assertEqual(len(data_points), 2)

        for i, data_point in enumerate(data_points):
            self.assertAlmostEqual(results[i], data_point.value, 1)

    def test_data_processing_init(self):
        can_id = 603
        can_data = "0000000011111111000000001111111100000000111111110000000011111111"

        config_list = [CanDataConfig(1, 1, 1, 1, "Temperature", "°C", "603", 0, 16, 0.5, 0, "B"),
                       CanDataConfig(2, 2, 2, 2, "Oil temperature", "°C", "603", 16, 16, 0.25, 0, "B"),
                       CanDataConfig(2, 2, 2, 2, "Speed", "km/hod", "600", 0, 16, 1, 0, "B")]

        self.assertRaises(TypeError, DataProcessing, can_id, can_data, config_list)

        can_id = "603"
        can_data = "0000000011111111"
        self.assertRaises(ValueError, DataProcessing, can_id, can_data, config_list)

        can_data = 100001001
        self.assertRaises(TypeError, DataProcessing, can_id, can_data, config_list)
