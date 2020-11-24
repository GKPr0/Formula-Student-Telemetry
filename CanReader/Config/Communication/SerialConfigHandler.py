from Config.ConfigHandler import ConfigHandler

class SerialConfigHandler(ConfigHandler):
    """
        This class has access to Communication config file.
        Can load config and return it as a list of CanDataConfig objects,
        or can update config sections from given CanDataConfig object.

        :param config_file_name: Name of config file.
        :type config_file_name: str

        :raises TypeError:
            - Config file name does not end with '.ini'.
            - Config file name contains disallowed symbols.
        :raises OSError:
            - Config file with given name does not exist.

    """