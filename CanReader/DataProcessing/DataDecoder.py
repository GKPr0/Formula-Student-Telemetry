class DataDecoder:
    """
        This class will receive ID, binary data and list of configs.
        \n
        As result will be list of objects called DataPoint.
        These objects will contain information like name, value, id and group id

        :param id: ID of CAN message
        :type id: int
        :param data: Data containing CAN message
        :type data: str
        :param config: Config is list of DataConfig object. DataConfig is described in Config section.
        :type config: DataConfig

        :raises TypeError: If id is not a int OR If data are not a str starting with '0b'
        :raises ValueError: If id is not in range 0 - 999

        - Example of valid constructor::

            config_list = Config.load_from_config_file()
            data_decoder = DataDecoder(100, "0b1111111111111111111111110111100010101010101110111100110011111000" , config_list )

    """
    def __init__(self, id, data, config):
        # Validate ID and Data
        self.check_id(id)
        self.check_data(data)

        self.__id = id
        self.__data = data

    def __repr__(self):
        return "ID: {} \t Data:{}".format(self.__id, self.__data)

    @staticmethod
    def check_id(id):
        try:
            if id < 0 or id > 999:
                raise ValueError
            if type(id) != int:
                raise TypeError
        except ValueError:
            raise ValueError("ID must be number in range of 0 - 999.")
        except TypeError:
            raise TypeError("ID must be integer.")

    @staticmethod
    def check_data(data):
        try:
            if type(data) != str or data[:2] != "0b":
                raise TypeError
        except TypeError:
            raise TypeError("Data must be binary")
