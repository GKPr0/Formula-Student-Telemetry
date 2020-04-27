from configparser import ConfigParser
from CanReader.Config.DataConfig import DataConfig
import re
import os
from pathlib import Path


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

    def __init__(self, config_file_name="config_file.ini"):
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

    def update_section_in_config(self, data_config):
        """
            Update config parameters for already existing variable.
            After updating save changes to file.

            :param data_config: Updated setting of variable
            :type data_config: DataConfig

            :raises TypeError:
                - Parameter data_config is not a DataConfig type.

        """
        self.check_update_parameter_type(data_config)

        section_id = str(data_config.id)

        if data_config.unit == "%":
            unit = "%%"
        else:
            unit = data_config.unit

        self.config.set(section_id, "Group id", str(data_config.group_id))
        self.config.set(section_id, "Widget id", str(data_config.widget_id))
        self.config.set(section_id, "Overview id", str(data_config.overview_id))
        self.config.set(section_id, "Name", data_config.name)
        self.config.set(section_id, "Unit", unit)
        self.config.set(section_id, "Can id", str(data_config.can_id))
        self.config.set(section_id, "Start bit", str(data_config.start_bit))
        self.config.set(section_id, "Length", str(data_config.length))
        self.config.set(section_id, "Multiplier", str(data_config.multiplier))
        self.config.set(section_id, "Offset", str(data_config.offset))

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
            data_config = self.load_selected_from_config_file(int(section))
            data_config_list.append(data_config)

        return data_config_list

    def load_selected_from_config_file(self, config_id):
        """

        :param config_id: id of data config that is supposed to be loaded
        :type config_id: int

        :return: data in form of object DataConfig for selected configuration
        :rtype: DataConfig

        :raises TypeError: config_id is not an integer

        :raises ValueError: config_id is greater then maximal id in config file

        """

        self.check_config_id(config_id)

        section = str(config_id)
        widget_id = self.config.getint(section, "Widget id")
        group_id = self.config.getint(section, "Group id")
        overview_id = self.config.getint(section, "Overview id")
        name = self.config.get(section, "Name")
        unit = self.config.get(section, "Unit")
        can_id = self.config.get(section, "Can id")
        start_bit = self.config.getint(section, "Start bit")
        length = self.config.getint(section, "Length")
        multiplier = self.config.getfloat(section, "Multiplier")
        offset = self.config.getfloat(section, "Offset")

        return DataConfig(config_id, group_id, widget_id, overview_id, name, unit, can_id, start_bit, length, multiplier, offset)

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
            raise TypeError("Config file can contain only A-Z, a-z , 0-9, _ and must ends with '.ini'")
        except OSError:
            raise OSError(config_file_name + " does not exist")

    @staticmethod
    def check_update_parameter_type(data_config):
        """
            Check type of data config
        """
        try:
            if type(data_config) != DataConfig:
                raise TypeError
        except TypeError:
            raise TypeError("As a parameter is expected DataConfig not " + type(data_config))

    @staticmethod
    def check_config_id(config_id):
        """
            Check type and value of config id that is supposed to be loaded
        """
        try:
            if type(config_id) != int:
                raise TypeError
            if config_id < 0 or config_id > Config().number_of_data_configs:
                raise ValueError
        except TypeError:
            raise TypeError("Config id must be integer")
        except ValueError:
            raise ValueError(
                "Config id must be in range of data config in config file {}".format(Config().number_of_data_configs))


if __name__ == "__main__":
    config = Config("config_file.ini")
    data_config_list = config.load_from_config_file()
    print(data_config_list)
