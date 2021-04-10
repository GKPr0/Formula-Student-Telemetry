from CanReader.DataProcessing.DataPoint import DataPoint
from CanReader.Exceptions.CanCheck import *


class DataProcessing:
    """
        :Description:
            This class takes ID, binary data and list of configs as input.\n
            Main task is to decode and processed binary data based on given config list.\n
            Resulting object will contain information like name, value, id and group id.

        :param can_id: Id of CAN message
        :type can_id: str
        :param can_data: CAN message in binary format
        :type can_data: str
        :param config_list: List of data configurations
        :type config_list: list[CanDataConfig]

        :raises TypeError:
            -- Can_id is not a hex string.\n
            -- Data is not a binary str.\n
        :raises ValueError:
            -- Can_id is hex string longer then 8.\n
            -- Can_data does not have length of 8 bytes (64 bits).\n
    """
    def __init__(self, can_id, can_data, config_list):
        # Validate ID and Data
        check_can_id(can_id)
        check_binary_can_data(can_data)

        self.__config_list = config_list
        self.__can_id = can_id
        self.__can_data = can_data

        self.__data_point_list = []

    def __repr__(self):
        return "ID: {} \t Data:{}".format(self.__can_id, self.__can_data)

    def data_decode(self):
        """
            :Description:
                Checks if there are data configurations for given can id.\n
                If so call processed data for each configuration
                where conf can id == given can id.\n
                As result return list of DataPoints,
                containing useful information as widget id, group id, name, value, etc.

            :return: List of DataPoints
            :rtype: list[DataPoint]
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
            :Description:
                Takes binary data and suitable data configuration as input.\n
                Based on given configuration processed data -> convert data from binary to real value.\n
                Conversion is done as follows:
                    1. Convert bin data to int in right format (Little or Big endian)
                    2. Multiply data by configuration multiplier
                    3. Add configuration offset

            :param bin_data: Can data in binary format.
            :type bin_data: str
            :param data_config: Suitable configuration
            :type data_config: CanDataConfig

            :return: Real value processed by given configuration
            :rtype: float
        """
        length = data_config.length
        start_bit = data_config.start_bit
        end_bit = start_bit + length
        multiplier = data_config.multiplier
        offset = data_config.offset

        if data_config.endian == "L" and length > 7:
            tmp = bin_data[start_bit:end_bit]
            data = [tmp[i*8:(i+1)*8] for i in range(int(len(tmp) / 8)-1, -1, -1)]
            data = int(''.join(map(str, data)), 2)
        else:
            data = int(bin_data[start_bit:end_bit], 2)
        return float((data * multiplier) + offset)
