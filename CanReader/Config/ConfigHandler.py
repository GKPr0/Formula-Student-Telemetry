import logging
import os
import re
from configparser import ConfigParser
from pathlib import Path


class ConfigHandler:
    """
        :Description:
            Base class for handling *.ini configs.

        :param config_file_name: Name of config file.
        :type config_file_name: str, optional

        :raises ValueError:
            -- Config file name does not end with '.ini'.\n
            -- Config file name contains disallowed symbols.\n
        :raises FileNotFoundError:
            Config file with given name does not exist.
    """

    def __init__(self, config_file_name):
        # Check config file name
        self.check_config_file(config_file_name)
        self.config_file_name = config_file_name
        self.config = ConfigParser()
        self.setup_config()

    def setup_config(self):
        """
            :Description:
                Load config and save number of config sections.
        """
        path = Path(__file__).parent.absolute()
        self.file_path = str(path) + "/" + self.config_file_name
        self.config.read(self.file_path)

        self.number_of_data_configs = len(self.config.sections())

    def save_config(self):
        """
            :Description:
                Save updated config.
        """
        with open(self.file_path, "w") as configfile:
            self.config.write(configfile)

    @staticmethod
    def check_config_file(config_file_name):
        """
            :Description:
                Check if config file exists and name ends with '.ini' and contains only allowed symbols A-Z, a-z ,0-9.

            :param config_file_name: Name of config file.
            :type config_file_name: str

            :raises ValueError:
                -- Config file name does not end with '.ini'.\n
                -- Config file name contains disallowed symbols.

            :raises FileNotFoundError:
                Config file with given name does not exist.
        """
        try:
            if not config_file_name.endswith(".ini"):
                raise ValueError
            if len(re.findall(r'[^A-Za-z0-9_\-\\]', config_file_name)) > 1:
                raise ValueError
            if not os.path.isfile(str(Path(__file__).parent.absolute()) + "/" + config_file_name):
                raise FileNotFoundError
        except ValueError:
            error_msg = "Config file can contain only A-Z, a-z , 0-9, _ and must ends with '.ini'"
            logging.exception(error_msg)
            raise ValueError(error_msg)
        except FileNotFoundError:
            error_msg = config_file_name + " does not exist"
            logging.exception(error_msg)
            raise FileNotFoundError(error_msg)
