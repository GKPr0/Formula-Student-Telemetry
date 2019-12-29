class DataDecoder:
    """
    This class will receive ID, binary data and list of configs.
    As result will be list of objects called Datapoint.
    These objects will contain information like name, value, id and group id
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
