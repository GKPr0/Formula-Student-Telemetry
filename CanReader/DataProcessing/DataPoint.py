class DataPoint:
    """
        This Class will contain variable information like name, value, id, group id
        \n
        Object will be used to update values in graphical interface

        :param id: id of widget in UI
        :type id: int
        :param group_id: id of display group in UI
        :type group_id: int
        :param name: name of variable
        :type name: str
        :param value: current value of variable
        :type value: float, int

        :raises TypeError:
            - ID or group_id are not an integer.
            - Name is not a str.
            - Value is not a float or int.
        :raises ValueError:
            - ID or group_id are not in range 0 - 999.
    """

    def __init__(self, id, group_id, name, value):
        self.id = id
        self.group_id = group_id
        self.__name = name
        self.value = value

    def __repr__(self):
        return "{} has id {}, is in group {} and have value {}\n".format(self.__name, self.id, self.group_id, self.value)
    
    @staticmethod
    def check_id(id):
        """
            Check validity of id. Expected to be int in range [0, 999]
        """
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
        """
            Check validity of group id. Expected to be int in range [0, 999]
        """
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
    def check_name(name):
        """
            Check validity of name. Expected to be str.
        """
        try:
            if type(name) != str:
                raise TypeError
        except TypeError:
            raise TypeError("Name must be string.")

    @staticmethod
    def check_value(value):
        """
            Check validity of value. Expected to be float or int
        """
        try:
            if type(value) not in [int, float]:
                raise TypeError
        except TypeError:
            raise TypeError("Value must be int or float")