from CanReader.Exceptions.CanCheck import *


class CanDataConfig:
    """
        :Description:
            This class contains data configuration.

        :param id: Unique id.
        :type id: int

        :param group_id: Id of display group in UI.
        :type group_id: int

        :param group_id: Id of widget in display group.
        :type group_id: int

        :param overview_id: Id of widget in overview tab.
        :type overview_id: int

        :param name: Name of variable.
        :type name: str

        :param unit: Unit type of value (°C, Km/h, ...)
        :type unit: str

        :param can_id: Id of can message.
        :type can_id: str

        :param start_bit: Bit on which data starts.
        :type start_bit: int

        :param length: Number of bits to read starting from start bit.
        :type length: int

        :param multiplier: Multiplier for data bounded with start bit and length.
        :type multiplier: float, int

        :param offset: Offset of value gained from bounded data with start bit and length.
        :type offset: float, int

        :param endian: Type of endian (Little, Big).
        :type endian: str

        :raises TypeError:
            -- Id is not an integer.\n
            -- Group id is not an integer.\n
            -- Widget id is not an integer.\n
            -- Overview id is not an integer.\n
            -- Name is not a str.\n
            -- Unit is not a str.\n
            -- Can_id is not a hex string.\n
            -- Start bit is not an integer.\n
            -- Length bit is not an integer.\n
            -- Multiplier is not an integer or float.\n
            -- Offset is not an integer or float.\n
            -- Endian is not a str.\n

        :raises ValueError:
            -- Group id is not in range 0 - 20.\n
            -- Widget id is not in range 1 - 50.\n
            -- Overview id is not in range 1 - 50.\n
            -- Can_id is hex string longer then 8.\n
            -- Start bit is not in range 0 - 63.\n
            -- Length is not in range 1 - 63.\n
            -- Multiplier is equal to 0.\n
            -- Endian is not a "L" or "B".\n

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
