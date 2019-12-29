

class RawData:
    """
    This class wil receive raw data split them into ID and data part.
    Data part will be converted to binary code with fixed length of 64 bit
    """

    DATA_START_BIT = 6  # Bit where starts data
    ID_START_BIT = 2  # Bit where start ID
    ID_LENGTH = 3   # Length of ID

    def __init__(self, raw_data):
        self.check_raw_data(raw_data)
        self.__raw_data = raw_data

    def __repr__(self):
        return "Raw_data: {}".format(self.__raw_data)

    def split_data(self):
        # Will pull ID and data from raw_data. Data will be converted to binary code with fixed length 64 bit.

        id = self.__raw_data[self.ID_START_BIT:(self.ID_START_BIT + self.ID_LENGTH)]
        data = bin(int(self.__raw_data[self.DATA_START_BIT:], 16))

        return id, data

    @staticmethod
    def check_raw_data(raw_data):
        try:
            if type(raw_data) != str:
                raise TypeError

        except TypeError:
            raise TypeError("Raw data are expected as string")



