from CanReader.Exceptions.CanCheck import *


class RawData:
    """
        :Description:
            This class takes raw received data from remote device.\n
            Used to split raw data into ID and data part.

        :param raw_data: Received data from remote device in its raw format.
        :type raw_data: bytearray

        :raises TypeError:
            Raw data are not a bytearray.
        :raises ValueError:
            Raw data do not have 12 bytes.
    """
    ID_BYTE_LENGTH = 4
    DATA_BYTE_LENGTH = 8

    def __init__(self, raw_data):
        check_raw_data(raw_data)
        self.__raw_data = raw_data

    def __repr__(self):
        return "Raw_data: {}".format(self.__raw_data)

    def split_data(self):
        """
            :Description:
                Split ID and data part from raw_data.\n
                Data will be returned in binary code with fixed length 64 bit.

            :returns:
                - ID (:py:class:`int`)
                - Data (:py:class:`str`) -> (in python bin is str with leading '0b')
        """

        id = self.__raw_data[:self.ID_BYTE_LENGTH].hex().lstrip("0")

        data = ["{:08b}".format(self.__raw_data[i]) for i in range(self.ID_BYTE_LENGTH, self.DATA_BYTE_LENGTH + self.ID_BYTE_LENGTH)]
        data = ''.join(map(str, data))

        return id, data
