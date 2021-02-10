import unittest

from CanReader.Config.ConfigHandler import ConfigHandler as Config


class ConfigTest(unittest.TestCase):
    """
        Unit test definition for class called Config.
    """

    def test_config_file_name(self):
        # Make sure config file name ends with '.ini' and contains only allowed symbols A-Z, a-z , 0-9 and _.
        self.assertRaises(ValueError, Config.check_config_file, "Tests.exe")
        self.assertRaises(ValueError, Config.check_config_file, "Tests")
        self.assertRaises(ValueError, Config.check_config_file, "T?est.ini")
        self.assertRaises(ValueError, Config.check_config_file, "T//?.ini")

    def test_config_file_existence(self):
        # Make sure config file already exists.
        self.assertRaises(FileNotFoundError, Config.check_config_file, "Tests.ini")
        self.assertRaises(FileNotFoundError, Config.check_config_file, "Neco_pod_carou.ini")
