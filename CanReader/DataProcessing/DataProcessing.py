from DataProcessing.DataPoint import DataPoint


class DataProcessing:
    """
        This class will receive ID, binary data and list of configs.
        \n
        As result will be list of objects called DataPoint, containing decoded and processed data.
        These objects will contain information like name, value, id and group id

        :param can_id: id of CAN message
        :type can_id: int
        :param can_data: data containing CAN message
        :type can_data: str
        :param config_list: config is list of DataConfig object. DataConfig is described in Config section.
        :type config_list: DataConfig

        :raises TypeError:
            - ID is not a int.
            - Data are not a binary str.
        :raises ValueError:
            - ID is not in range 0 - 999.
    """
    def __init__(self, can_id, can_data, config_list):
        # Validate ID and Data
        self.check_id(can_id)
        self.check_data(can_data)

        self.__config_list = config_list
        self.__can_id = can_id
        self.__can_data = can_data

        self.__data_point_list = []

    def __repr__(self):
        return "ID: {} \t Data:{}".format(self.__can_id, self.__can_data)

    def data_decode(self):
        """
            Check if given can id is in configuration
            If so it will call method data_process(), for data processing.
            For every configuration where can id == given can id, create new DataPoint

            :return: List of DataPoints, that contains ( widget id ,group id , name and value)
            :rtype: DataPoint
        """
        for data_config in self.__config_list:
            if data_config.can_id == self.__can_id:
                widget_id = data_config.widget_id
                group_id = data_config.group_id
                overview_id = data_config.overview_id
                name = data_config.name
                value = self.data_process(self.__can_data, data_config)

                data_point = DataPoint(widget_id, group_id, overview_id, name, value)
                self.__data_point_list.append(data_point)

        return self.__data_point_list

    @staticmethod
    def data_process(bin_data, data_config):
        """
            Take binary data and suitable data configuration.
            Suitability of configuration is established by corespondent can id-> Done by method caller
            Part of data (config choose which part) is converted from bin to dec.
            Decimal number is multiplied by configuration multiplier and magnified by configuration offset

            :param bin_data: Can data in binary form with fixed 64 bit length
            :type bin_data: str
            :param data_config: Configuration
            :type data_config: DataConfig
            :return: Decoded and processed value corresponding to configuration
        """
        start_bit = data_config.start_bit
        end_bit = start_bit + data_config.length
        multiplier = data_config.multiplier
        offset = data_config.offset

        if data_config.endian == "L":
            tmp = bin_data[start_bit:end_bit]
            data = [tmp[i*8:(i+1)*8] for i in range(int(len(tmp) / 8)-1, -1, -1)]
            data = int(''.join(map(str, data)), 2)
        else:
            data = int(bin_data[start_bit:end_bit], 2)
        return float((data * multiplier) + offset)

    @staticmethod
    def check_id(can_id):
        """
            Check if id is valid. Expected hex string in range [0, 999]
        """
        try:
            if type(can_id) != str:
                raise TypeError
        except ValueError:
            raise ValueError("ID must be number in range of 0 - 999.")
        except TypeError:
            raise TypeError("ID must be string.")

    @staticmethod
    def check_data(data):
        """
            Check if data are valid. Expected binary string'
        """
        try:
            if type(data) != str:
                raise TypeError
        except TypeError:
            raise TypeError("Data must be binary string")
