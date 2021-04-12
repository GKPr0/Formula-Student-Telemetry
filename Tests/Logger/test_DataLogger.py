import unittest

from CanReader.Logger.DataLogger import DataLogger
from datetime import datetime

class TestDataLogger(unittest.TestCase):

    def test_push_raw_data(self):
        loger = DataLogger()

        loger.push_raw_can("603", "156")
        loger.push_raw_can("604", "1056")
        loger.push_raw_can("603", "1560")
        loger.push_raw_can("603", "1560")
        loger.push_raw_can("603", "1560")
        loger.push_raw_can("600", "15648")
        loger.push_raw_can("603", "156")

        self.assertEqual(3, len(loger.can_dict))
        self.assertEqual("156", loger.can_dict["603"])
        self.assertEqual("15648", loger.can_dict["600"])
        self.assertEqual("1056", loger.can_dict["604"])

        self.assertEqual(5, len(loger.raw_data))
