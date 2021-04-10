from CanReader.Config.ConfigHandler import ConfigHandler


class ComConfigHandler(ConfigHandler):
    """
        :Inherit: :class:`ConfigHandler`

        :Description:
            Main task is to handle Com config file.\n

        :param config_file_name:
            Name of config file.
        :type config_file_name:
            str, optional

        :raises:
            For error handling see base class :class:`ConfigHandler`.
    """

    def __init__(self, config_file_name="communication_config.ini"):
        ConfigHandler.__init__(self, config_file_name=config_file_name)

    def load_serial_info(self):
        """
            :Description:
                Load current serial com config.

            :returns:
                - Port (:py:class:`str`)
                - BaudRate (:py:class:`int`)
        """
        port = self.config.get("serial", "port")
        baud_rate = self.config.getint("serial", "baud rate")

        return port, baud_rate

    def update_serial_info(self, port, baud_rate):
        """
            :Description:
                Update serial com config.

            :param port: Name of com port.
            :type port: str

            :param baud_rate: Desired baud rate.
            :type baud_rate: int
        """
        self.config.set("serial", "port", str(port))
        self.config.set("serial", "baud rate", str(baud_rate))
        self.save_config()

    def load_wifi_info(self):
        """
            :Description:
                Load current Wi-Fi com config.

            :returns:
                - Ip (:py:class:`str`)
                - Port (:py:class:`int`)
        """
        ip = self.config.get("wifi", "ip")
        port = self.config.getint("wifi", "port")

        return ip, port

    def update_wifi_info(self, ip, port):
        """
            :Description:
                Update Wi-Fi com config.

            :param ip: Ip address of remote device.
            :type ip: str

            :param port: Port on which devices will communicate.
            :type port: int
        """
        self.config.set("wifi", "ip", str(ip))
        self.config.set("wifi", "port", str(port))
        self.save_config()
