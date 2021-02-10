from CanReader.Exceptions.CanCheck import *


class CanDataConfig:
    """
        This class will contain data configuration.
        Data configuration are ID, Group id , Name, Unit, Can id, Start bit, length, Multiplier, Offset

        :param id: unique id
        :type id: int
        :param group_id: id of display group in UI
        :type group_id: int
        :param group_id: id of widget in tab
        :type group_id: int
        :param name: name of variable
        :type name: str
        :param unit: unit type of value (°C, Km/h, ...)
        :type unit: str
        :param can_id: id of can message, on which is supposed to look for incoming data
        :param can_id: string
        :param start_bit: bit on which start data for selected variable
        :type start_bit: int
        :param length: number of bits to read from start bit
        :type length: int
        :param multiplier: multiplier for data bounded with start bit and length
        :type multiplier: float, int
        :param offset: offset of value gained from bounded data with start bit and length
        :type offset: float, int

        :raises TypeError:
            - ID, group_id, widget_id or can_id are not an integer.
            - Name is not a str.
            - Value is not a float or an int

        :raises ValueError:
            - ID or can_id are not in range 0 - 999
            - Group_id or widget_id are not in range 1-10
    """

    def __init__(self, id, group_id, widget_id, overview_id, name, unit, can_id,
                 start_bit, length, multiplier, offset, endian):
        # Check validity of parameters
        check_id(id)
        check_group_id(group_id)
        check_widget_id(widget_id)
        check_widget_id(overview_id)
        check_can_id(can_id)
        check_name(name)
        check_unit(unit)
        check_start_bit(start_bit)
        check_length(length)
        check_multiplier(multiplier)
        check_offset(offset)
        check_endian(endian)

        self.id = id
        self.group_id = group_id
        self.widget_id = widget_id
        self.overview_id = overview_id
        self.name = name
        self.unit = unit
        self.can_id = can_id
        self.start_bit = start_bit
        self.length = length
        self.multiplier = multiplier
        self.offset = offset
        self.endian = endian

    def __repr__(self):
        return "ID: {} \nGroup ID: {} \nWidget ID: {} \n Name: {} \nUnit: {} \nCan ID: {}" \
               " \nStart bit: {} \nLength: {} \nMultiplier {} \nOffset {} \n Endian {} \n" \
            .format(self.id, self.group_id, self.widget_id, self.name, self.unit, self.can_id,
                    self.start_bit, self.length, self.multiplier, self.offset, self.endian)
