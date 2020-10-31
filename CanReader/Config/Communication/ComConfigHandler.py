from Config.ConfigHandler import ConfigHandler


class ComConfigHandler(ConfigHandler):
    """
        This class has access to Communication config file.

        :param config_file_name: Name of config file.
        :type config_file_name: str

        :raises TypeError:
            - Config file name does not end with '.ini'.
            - Config file name contains disallowed symbols.
        :raises OSError:
            - Config file with given name does not exist.

    """

    def __init__(self, config_file_name="communication_config.ini"):
        ConfigHandler.__init__(self, config_file_name=config_file_name)

    def load_serial_info(self):
        port = self.config.get("serial", "port")
        baud_rate = self.config.getint("serial", "baud rate")

        return port, baud_rate

    def update_serial_info(self, port, baud_rate):
        self.config.set("serial", "port", str(port))
        self.config.set("serial", "baud rate", str(baud_rate))
        self.save_config()

    def load_wifi_info(self):
        ip = self.config.get("wifi", "ip")
        port = self.config.getint("wifi", "port")

        return ip, port

    def update_wifi_info(self, ip, port):
        self.config.set("wifi", "ip", str(ip))
        self.config.set("wifi", "port", str(port))
        self.save_config()
