import unittest
import os


from CanReader.Config.ConfigHandler import ConfigHandler


class TestConfigHandler(unittest.TestCase):
    """
        Unit test definition for class called Config.
    """

    def test_config_file_name(self):
        # Make sure config file name ends with '.ini' and contains only allowed symbols A-Z, a-z , 0-9 and _.
        self.assertRaises(ValueError, ConfigHandler.check_config_file, "Tests.exe")
        self.assertRaises(ValueError, ConfigHandler.check_config_file, "Tests")
        self.assertRaises(ValueError, ConfigHandler.check_config_file, "T?est.ini")
        self.assertRaises(ValueError, ConfigHandler.check_config_file, "T//?.ini")

    def test_config_file_existence(self):
        # Make sure config file already exists.
        self.assertRaises(FileNotFoundError, ConfigHandler.check_config_file, "Tests.ini")
        self.assertRaises(FileNotFoundError, ConfigHandler.check_config_file, "Neco_pod_carou.ini")

        root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        for file in os.listdir(os.path.join(root_path, "CanReader/Config")):
            if file.endswith(".ini"):
                ConfigHandler.check_config_file(file)
