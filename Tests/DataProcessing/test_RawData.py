import unittest

from CanReader.DataProcessing.RawData import RawData


class TestRawData(unittest.TestCase):

    def test_raw_data_init(self):

        raw_data = [255, 128, 0, 145, 12, 58, 68, 0, 0, 0, 7, 128]
        self.assertRaises(TypeError, RawData, raw_data)

        raw_data = bytearray([255, 128, 0, 145, 12, 58, 68, 0, 0, 0, 7])
        self.assertRaises(ValueError, RawData, raw_data)

    def test_raw_data_split(self):
        raw_data = bytearray([0, 0, 6, 3, 128, 00, 64, 0, 255, 0, 32, 0])

        can_id, can_data = RawData(raw_data).split_data()

        self.assertIsInstance(can_data, str)
        self.assertIsInstance(can_id, str)
        self.assertEqual("603", can_id)
        self.assertEqual(64, len(can_data))

        raw_data = bytearray([255, 0, 6, 3, 0, 00, 0, 0, 0, 0, 0, 0])

        can_id, can_data = RawData(raw_data).split_data()

        self.assertIsInstance(can_data, str)
        self.assertIsInstance(can_id, str)
        self.assertEqual("ff000603", can_id)
        self.assertEqual(64, len(can_data))
