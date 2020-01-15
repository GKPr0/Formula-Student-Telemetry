class DataConfig:
    """
        This class will contain data configuration.
        Data configuration are ID, Group id , Name, Unit, Can id, Start bit, length, Multiplier, Offset

        :param id: id of widget in UI
        :type id: int
        :param group_id: id of display group in UI
        :type group_id: int
        :param name: name of variable
        :type name: str
        :param unit: unit type of value (°C, Km/h, ...)
        :type unit: str
        :param can_id: id of can message, on which is supposed to look for incoming data
        :param can_id: int
        :param start_bit: bit on which start data for selected variable
        :type start_bit: int
        :param length: number of bits to read from start bit
        :type length: int
        :param multiplier: multiplier for data bounded with start bit and length
        :type multiplier: float, int
        :param offset: offset of value gained from bounded data with start bit and length
        :type offset: float, int

        :raises TypeError:
            - ID or group_id are not an integer.
            - Name is not a str.
            - Value is not a float or an int

        :raises ValueError:
            - ID or group_id are not in range 0 - 999
    """
    def __init__(self,id, group_id, name, unit, can_id, start_bit, length, multiplier, offset):
        # Check validity of parameters
        self.check_id(id)
        self.check_group_id(group_id)
        self.check_can_id(can_id)
        self.check_name(name)
        self.check_unit(unit)
        self.check_start_bit(start_bit)
        self.check_length(length)
        self.check_multiplier(multiplier)
        self.check_offset(offset)

        self.id = id
        self.group_id = group_id
        self.name = name
        self.unit = unit
        self.can_id = can_id
        self.start_bit = start_bit
        self.length = length
        self.multiplier = multiplier
        self.offset = offset


    @staticmethod
    def check_id(id):
        # Check validity of ID. Works for id, group id and can id
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
    def check_group_id(id):
        # Check validity of group id
        try:
            if id < 0 or id > 999:
                raise ValueError
            if type(id) != int:
                raise TypeError
        except ValueError:
            raise ValueError("Group id must be number in range of 0 - 999.")
        except TypeError:
            raise TypeError("Group id must be integer.")

    @staticmethod
    def check_can_id(id):
        # Check validity of can id
        try:
            if id < 0 or id > 999:
                raise ValueError
            if type(id) != int:
                raise TypeError
        except ValueError:
            raise ValueError("Can id must be number in range of 0 - 999.")
        except TypeError:
            raise TypeError("Can id must be integer.")

    @staticmethod
    def check_name(name):
        # Check validity of name
        try:
            if type(name) != str:
                raise TypeError
        except TypeError:
            raise TypeError("Name must be string.")

    @staticmethod
    def check_unit(unit):
        # Check validity of unit
        try:
            if type(unit) != str:
                raise TypeError
        except TypeError:
            raise TypeError("Unit must be string.")

    @staticmethod
    def check_start_bit(start_bit):
        # Check validity of star bit
        try:
            if type(start_bit) != int:
                raise TypeError
            if start_bit < 0 or start_bit > 63:
                raise ValueError
        except TypeError:
            raise TypeError("Start bit must be integer")
        except ValueError:
            raise ValueError("Start bit must be number in range of 0 - 63")

    @staticmethod
    def check_length(length):
        # Check validity of length
        try:
            if type(length) != int:
                raise TypeError
            if length < 1 or length > 63:
                raise ValueError
        except TypeError:
            raise TypeError("Length must be integer")
        except ValueError:
            raise ValueError("Length must be in range of 1 - 63")

    @staticmethod
    def check_multiplier(multiplier):
        # Check validity of multiplier
        try:
            if type(multiplier) not in [int, float]:
                raise TypeError
            if multiplier <= 0:
                raise ValueError
        except TypeError:
            raise TypeError("Multiplier must be integer or float.")
        except ValueError:
            raise ValueError("Multiplier cannot be negative number.")

    @staticmethod
    def check_offset(offset):
        # Check validity of offset
        try:
            if type(offset) not in [int, float]:
                raise TypeError
        except TypeError:
            raise TypeError("Offset must be integer or float.")
