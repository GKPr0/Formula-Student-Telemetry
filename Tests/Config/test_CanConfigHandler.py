import unittest

from CanReader.Config.CanBus.CanConfigHandler import CanConfigHandler
from CanReader.Config.CanBus.CanDataConfig import CanDataConfig


class TestCanConfigHandler(unittest.TestCase):

    def test_check_update_parameter_type(self):
        # Make sure config is of type CanDataConfig
        self.assertRaises(TypeError, CanConfigHandler.check_update_parameter_type, 4)
        self.assertRaises(TypeError, CanConfigHandler.check_update_parameter_type, 4.5)
        self.assertRaises(TypeError, CanConfigHandler.check_update_parameter_type, "aaa")
        self.assertRaises(TypeError, CanConfigHandler.check_update_parameter_type, [0, 15])
        self.assertRaises(TypeError, CanConfigHandler.check_update_parameter_type, True)
        self.assertRaises(TypeError, CanConfigHandler.check_update_parameter_type, None)

        test_data = CanDataConfig(2, 0, 1, 1, "Temperature", "°C", "605", 0, 16, 1, 0, "B")
        CanConfigHandler.check_update_parameter_type(test_data)

    def test_check_config_id_type(self):
        # Make sure config id is int
        self.assertRaises(TypeError, CanConfigHandler.check_config_id, "aa")
        self.assertRaises(TypeError, CanConfigHandler.check_config_id, 2.3)
        self.assertRaises(TypeError, CanConfigHandler.check_config_id, True)
        self.assertRaises(TypeError, CanConfigHandler.check_config_id, None)
        self.assertRaises(TypeError, CanConfigHandler.check_config_id, [0, 16])
        self.assertRaises(TypeError, CanConfigHandler.check_config_id, '52.3')

    def test_check_config_id_value(self):
        # Make sure config id in range 0 - NUMBER_OF_CONFIGS
        number_of_configs = CanConfigHandler().number_of_data_configs

        self.assertRaises(ValueError, CanConfigHandler.check_config_id, -1)
        self.assertRaises(ValueError, CanConfigHandler.check_config_id, number_of_configs + 1)

        CanConfigHandler.check_config_id(0)
        CanConfigHandler.check_config_id(round(number_of_configs/2))
        CanConfigHandler.check_config_id(number_of_configs)

    def test_load_selected_from_config_file(self):
        # Make sure config can load selected data in proper format
        can_config = CanConfigHandler()
        number_of_configs = can_config.number_of_data_configs

        for i in range(1, number_of_configs):
            can_data_config = can_config.load_selected_from_config_file(i)
            self.assertTrue(type(can_data_config) is CanDataConfig)


    def test_load_from_config_file(self):
        # Make sure config can load all data in proper format
        can_config = CanConfigHandler()
        number_of_configs = can_config.number_of_data_configs

        can_data_config_list = can_config.load_from_config_file()

        self.assertEqual(len(can_data_config_list), number_of_configs)

        for data_config in can_data_config_list:
            self.assertTrue(type(data_config) is CanDataConfig)
