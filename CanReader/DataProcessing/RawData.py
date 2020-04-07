
class RawData:
    """
        This class wil receive raw data and split them into ID and data part.

        :param raw_data: Raw data contains received data from remote device in its raw format
        :type raw_data: str

        :raises TypeError:
            - Rawdata are not a str.

        - Example of valid constructor::

            raw_data = RawData("ID100XFFFFFF78AABBCCF8")

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
        """
        Will pull ID and data part from raw_data.
        Data will be converted from hex to binary code with fixed length 64 bit.

        :returns:
            - ID (:py:class:`str`)
            - Data (:py:class:`str`) -> (in python bin is str with leading '0b')

        - Example of valid method output::

            raw_data = RawData("ID100XFFFFFF78AABBCCF8")
            [id , data] = raw_data.split_data()

            id = 100
            data = "0b1111111111111111111111110111100010101010101110111100110011111000"
        """

        id = str(self.__raw_data[self.ID_START_BIT:(self.ID_START_BIT + self.ID_LENGTH)])
        data = bin(int(self.__raw_data[self.DATA_START_BIT:], 16))[2:].zfill(64)

        return id, data

    @staticmethod
    def check_raw_data(raw_data):
        """
            Check validity of raw_data type, str is expected.
        """

        try:
            if type(raw_data) != str:
                raise TypeError

        except TypeError:
            raise TypeError("Raw data are expected as string")



