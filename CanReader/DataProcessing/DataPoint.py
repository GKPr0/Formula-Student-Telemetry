from CanReader.Exceptions.CanCheck import *


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

    def __init__(self, id, group_id, overview_id, name, value):
        check_widget_id(id)
        check_group_id(group_id)
        check_widget_id(overview_id)
        check_name(name)
        check_value(value)

        self.id = id
        self.group_id = group_id
        self.overview_id = overview_id
        self.name = name
        self.value = value

    def __repr__(self):
        return "{} has id {}, is in group {} and have value {}. It´s overview id is {}\n"\
            .format(self.name, self.id, self.group_id, self.value, self.overview_id)
