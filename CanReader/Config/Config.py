from configparser import ConfigParser
from CanReader.Config.DataConfig import DataConfig
import re
import os

class Config:
    """
        This class has access to config file.
        Can load config and return it as a list of DataConfig objects,
        or can update config sections from given DataConfig object.

        :param config_file_name: Name of config file.
        :type config_file_name: str

        :raises TypeError:
            - Config file name does not end with '.ini'.
            - Config file name contains disallowed symbols.
        :raises OSError:
            - Config file with given name does not exist.

    """

    def __init__(self, config_file_name = "config_file.ini"):
        #Check config file name
        self.check_config_file(config_file_name)

        self.config_file_name = config_file_name
        self.config = ConfigParser()
        self.config.read(self.config_file_name)

    def save_config(self):
        """
            Save updated config
        """
        with open(self.config_file_name, "w") as configfile:
            self.config.write(configfile)

    def update_section_in_config(self, data_config):
        """
            Update config parameters for already existing variable.
            After updating save changes to file.

            :param data_config: Updated setting of variable
            :type data_config: DataConfig

            :raises TypeError:
                - Parameter data_config is not a DataConfig type.

        """
        self.check_update_parametr_type(data_config)

        section_id = str(data_config.id)

        self.config.set(section_id, "Group id", data_config.group_id)
        self.config.set(section_id, "Name", data_config.name)
        self.config.set(section_id, "Unit", data_config.unit)
        self.config.set(section_id, "Can id", data_config.can_id)
        self.config.set(section_id, "Start bit", data_config.start_bit)
        self.config.set(section_id, "Length", data_config.length)
        self.config.set(section_id, "Multiplier", data_config.multiplier)
        self.config.set(section_id, "Offset", data_config.offset)

        self.save_config()

    def load_from_config_file(self):
        """
            Load every section saved in config file to DataConfig objects.

            :return: List of DataConfig object.
            :rtype: DataConfig
        """
        data_config_list = []
        sections = self.config.sections()

        for section in sections:
            id = int(section)
            group_id = self.config.getint(section, "Group id")
            name = self.config.get(section, "Name")
            unit = self.config.get(section, "Unit")
            can_id = self.config.getint(section, "Can id")
            start_bit = self.config.getint(section, "Start bit")
            length = self.config.getint(section, "Length")
            multiplier = self.config.getfloat(section, "Multiplier")
            offset = self.config.getfloat(section, "Offset")

            data_config = DataConfig(id, group_id, name, unit, can_id, start_bit, length, multiplier, offset)
            data_config_list.append(data_config)

        return data_config_list

    @staticmethod
    def check_config_file(config_file_name):
        # Check if config file name ends with '.ini' and contains only allowed symbols A-Z, a-z , 0-9 and _
        try:
            if not config_file_name.endswith(".ini"):
                raise TypeError
            if len(re.findall(r'[^A-Za-z0-9_\-\\]', config_file_name)) > 1:
                raise TypeError
            if not os.path.isfile(config_file_name):
                raise OSError
        except TypeError:
            raise TypeError("Config file can contain only A-Z, a-z , 0-9, _ and must ends with '.ini'")
        except OSError:
            raise OSError(config_file_name + " does not exist")

    @staticmethod
    def check_update_parametr_type(data_config):
        try:
            if type(data_config) != DataConfig:
                raise TypeError
        except TypeError:
            raise TypeError("As a parameter is expected DataConfig not " + type(data_config))



if __name__ == "__main__":
    config = Config("kokot.ini")
    data_config_list = config.load_from_config_file()
    print(data_config_list)





