from configparser import ConfigParser
import re
import logging
import os
from pathlib import Path


class ConfigHandler:
    """
        Parent class for specific *.ini configs.
        Use only inheritance classes!

        :param config_file_name: Name of config file.
        :type config_file_name: str

        :raises TypeError:
            - Config file name does not end with '.ini'.
            - Config file name contains disallowed symbols.
        :raises OSError:
            - Config file with given name does not exist.

    """

    def __init__(self, config_file_name):
        # Check config file name
        self.check_config_file(config_file_name)
        self.config_file_name = config_file_name
        self.config = ConfigParser()
        self.setup_config()

    def setup_config(self):
        """
            Setup path to config file
        """
        path = Path(__file__).parent.absolute()
        self.file_path = str(path) + "/" + self.config_file_name
        self.config.read(self.file_path)

        self.number_of_data_configs = len(self.config.sections())

    def save_config(self):
        """
            Save updated config
        """
        with open(self.file_path, "w") as configfile:
            self.config.write(configfile)

    @staticmethod
    def check_config_file(config_file_name):
        """
            Check if config file name ends with '.ini' and contains only allowed symbols A-Z, a-z , 0-9 and
        """
        try:
            if not config_file_name.endswith(".ini"):
                raise TypeError
            if len(re.findall(r'[^A-Za-z0-9_\-\\]', config_file_name)) > 1:
                raise TypeError
            if not os.path.isfile(str(Path(__file__).parent.absolute()) + "/" + config_file_name):
                raise OSError
        except TypeError:
            logging.exception("Config file can contain only A-Z, a-z , 0-9, _ and must ends with '.ini'")
        except OSError:
            logging.exception(config_file_name + " does not exist")
