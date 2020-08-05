
class RawData:
    """
        This class wil receive raw data and split them into ID and data part.

        :param raw_data: Raw data contains received data from remote device in its raw format
        :type raw_data: bytearray

        :raises TypeError:
            - Rawdata are not a bytearray.
    """
    ID_BYTE_LENGTH = 4
    DATA_BYTE_LENGTH = 8

    def __init__(self, raw_data):
        self.check_raw_data(raw_data)
        self.__raw_data = raw_data

    def __repr__(self):
        return "Raw_data: {}".format(self.__raw_data)

    def split_data(self):
        """
        Will pull ID and data part from raw_data.
        Data will be returned in binary code with fixed length 64 bit.

        :returns:
            - ID (:py:class:`int`)
            - Data (:py:class:`str`) -> (in python bin is str with leading '0b')
        """

        id = int.from_bytes(self.__raw_data[:self.ID_BYTE_LENGTH], "big")
        #print(bin(int("00A5FFFFBFFCFF", 16))[2:].zfill(64))

        data = ["{:08b}".format(self.__raw_data[i]) for i in range(self.ID_BYTE_LENGTH, self.DATA_BYTE_LENGTH + self.ID_BYTE_LENGTH)]
        data = ''.join(map(str, data))

        return id, data

    @staticmethod
    def check_raw_data(raw_data):
        """
            Check validity of raw_data type, str is expected.
        """

        try:
            if type(raw_data) != bytearray:
                raise TypeError

        except TypeError:
            raise TypeError("Raw data are expected as bytearray")
