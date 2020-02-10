import unittest
from CanReader.Config.Config import Config


class ConfigTest(unittest.TestCase):
    """
        Unit test definition for class called Config.
    """
    def test_config_file_name(self):
        # Make sure config file name ends with '.ini' and contains only allowed symbols A-Z, a-z , 0-9 and _.
        self.assertRaises(TypeError, Config.check_config_file, "Test.exe")
        self.assertRaises(TypeError, Config.check_config_file, "Test")
        self.assertRaises(TypeError, Config.check_config_file, "T?est.ini")
        self.assertRaises(TypeError, Config.check_config_file, "T//?.ini")

    def test_config_file_existence(self):
        # Make sure config file already exists.
        self.assertRaises(OSError, Config.check_config_file, "Test.ini")
        self.assertRaises(OSError, Config.check_config_file, "Neco_pod_carou.ini")


    def test_update_function_parameter(self):
        # Make sure parameter in method update_section_in_config is DataConfig type.
        self.assertRaises(TypeError, Config.check_update_parameter_type, 123)
        self.assertRaises(TypeError, Config.check_update_parameter_type, 12.3)
        self.assertRaises(TypeError, Config.check_update_parameter_type, "str")
        self.assertRaises(TypeError, Config.check_update_parameter_type, True)

    def test_config_id_value(self):
        # Make sure id is in valid range 0 - 999
        self.assertRaises(ValueError, Config.check_config_id, 1000)
        self.assertRaises(ValueError, Config.check_config_id, -1)

    def test_config_id_type(self):
        # Make sure id is integer
        self.assertRaises(TypeError, Config.check_config_id, True)
        self.assertRaises(TypeError, Config.check_config_id, 15.6)
        self.assertRaises(TypeError, Config.check_config_id, "String")
        self.assertRaises(TypeError, Config.check_config_id, 'a')



