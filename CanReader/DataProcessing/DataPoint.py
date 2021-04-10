from CanReader.Exceptions.CanCheck import *


class DataPoint:
    """
        :Description:
            This Class contains data information like name, value, id, group id and overview id.\n
            Containing data are being used to update values in graphical interface.

        :param id: Id of widget in display group
        :type id: int
        :param group_id: Id of display group in UI
        :type group_id: int
        :param name: Name of variable
        :type name: str
        :param value: Real value.
        :type value: float, int

        :raises TypeError:
            -- Widget id is not an integer.\n
            -- Overview id is not an integer.\n
            -- Group id is not an integer.\n
            -- Name is not a str.\n
            -- Value is not a float or int.\n
        :raises ValueError:
            -- Widget id is not in range 1 - 50.\n
            -- Overview id is not in range 1 - 50.\n
            -- Group id is not in range 0 - 20.\n
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
