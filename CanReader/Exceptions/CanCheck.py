import logging


def check_id(id):
    """
        :Description:
            Id is expected to by of type int.

        :param id: General Id.
        :type id: int

        :raises TypeError:
            Id is not an integer.
    """
    try:
        if type(id) != int:
            raise TypeError
    except TypeError:
        error_msg = "ID must be integer."
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_group_id(group_id):
    """
        :Description:
            Group id is expected to by of type int.

        :param group_id: Group ID in UI.
        :type group_id: int

        :raises TypeError:
            Group id is not an integer.

        :raises ValueError:
            Group id is not in range 0 - 20.
    """
    try:
        if type(group_id) != int:
            raise TypeError
        if group_id < 0 or group_id > 20:
            raise ValueError
    except ValueError:
        error_msg = "Group id must be number in range of 0 - 999."
        logging.exception(error_msg)
        raise ValueError(error_msg)
    except TypeError:
        error_msg = "Group id must be integer."
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_widget_id(widget_id):
    """
        :Description:
            Widget id is expected to by of type int.

        :param widget_id: Widget id in display group of UI.
        :type widget_id: int

        :raises TypeError:
            Widget id is not an integer.

        :raises ValueError:
            Widget id is not in range 1 - 50.
    """
    try:
        if type(widget_id) != int:
            raise TypeError
        if widget_id < 0 or widget_id > 50:
            raise ValueError
    except ValueError:
        error_msg = "Widget id must be number in range of 1 - 50."
        logging.exception(error_msg)
        raise ValueError(error_msg)
    except TypeError:
        error_msg = "Widget id must be integer."
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_can_id(can_id):
    """
        :Description:
            Can id is expected to be HEX string of max len 8.

        :param can_id: Can id in hex format.
        :type can_id: str

        :raises TypeError:
            Can_id is not a hex string.

        :raises ValueError:
            Can_id is hex string longer then 8.
    """
    try:
        if type(can_id) != str:
            raise TypeError
        int(can_id, 16)
        if len(can_id) > 8:
            raise ValueError
    except TypeError:
        error_msg = "Can ID must be a hex string"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "CAN ID must be hex of max length 8"
        logging.exception(error_msg)
        raise ValueError(error_msg)


def check_name(name):
    """
        :Description:
            Name is expected to by of type str.

        :param name: Name of data variable.
        :type name: str

        :raises TypeError:
            Name is not a str.
    """
    try:
        if type(name) != str:
            raise TypeError
    except TypeError:
        error_msg = "Name must be string."
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_unit(unit):
    """
        :Description:
            Unit is expected to by of type str.

        :param unit: Data unit(°C, Pa, ...).
        :type unit: str

        :raises TypeError:
            Unit is not a str.
    """
    try:
        if type(unit) != str:
            raise TypeError
    except TypeError:
        error_msg = "Unit must be string."
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_start_bit(start_bit):
    """
        :Description:
            Start bit is expected to be of type int in range of 0 - 63.

        :param start_bit: Data start bit in can msg.
        :type start_bit: int

        :raises TypeError:
            Start bit is not an integer.

        :raises ValueError:
            Start bit is not in range 0 - 63.
    """
    try:
        if type(start_bit) != int:
            raise TypeError
        if start_bit < 0 or start_bit > 63:
            raise ValueError
    except TypeError:
        error_msg = "Start bit must be integer"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "Start bit must be number in range of 0 - 63"
        logging.exception(error_msg)
        raise ValueError(error_msg)


def check_length(length):
    """
        :Description:
            Length is expected to by of type int in range of 1 - 63.

        :param length: Data length in can msg.
        :type length: int

        :raises TypeError:
            Length bit is not an integer.

        :raises ValueError:
            Length is not in range 1 - 63.
    """
    try:
        if type(length) != int:
            raise TypeError
        if length < 1 or length > 63:
            raise ValueError
    except TypeError:
        error_msg = "Length must be integer"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "Length must be in range of 1 - 63"
        logging.exception(error_msg)
        raise ValueError(error_msg)


def check_multiplier(multiplier):
    """
        :Description:
            Multiplier is expected to by of type float or int.\n
            Cannot be equal to 0.

        :param multiplier: Data multiplier in can msg.
        :type multiplier: int, float

        :raises TypeError:
            Multiplier is not an integer or float.

        :raises ValueError:
            Multiplier is equal to 0.
    """
    try:
        if type(multiplier) not in [int, float]:
            raise TypeError
        if multiplier == 0:
            raise ValueError
    except TypeError:
        error_msg = "Multiplier must be integer or float."
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "Multiplier cannot be zero."
        logging.exception(error_msg)
        raise ValueError(error_msg)


def check_offset(offset):
    """
        :Description:
            Offset is expected to by of type float or int.

        :param offset: Data offset in can msg.
        :type offset: int, float

        :raises TypeError:
            Offset is not an integer or float.
    """
    try:
        if type(offset) not in [int, float]:
            raise TypeError
    except TypeError:
        error_msg = "Offset must be integer or float."
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_endian(endian):
    """
        :Description:
            Endian is expected as "L" or "B" of type str.

        :param endian: Little or Big endian.
        :type endian: str

        :raises TypeError:
            Endian is not a str.

        :raises ValueError:
            Endian is not a "L" or "B".
    """
    try:
        if type(endian) != str:
            raise TypeError
        if endian not in ["L", "B"]:
            raise ValueError
    except TypeError:
        error_msg = "Endian must be string"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "Endian is expected as 'L' or 'B'"
        logging.exception(error_msg)
        raise ValueError(error_msg)


def check_value(value):
    """
        :Description:
            Value is expected to be of type float or int.

        :param value: Real data value.
        :type value: int, float

        :raises TypeError:
            Value is not an integer or float.
    """
    try:
        if type(value) not in [int, float]:
            raise TypeError
    except TypeError:
        error_msg = "Value must be int or float"
        logging.exception(error_msg)
        raise TypeError(error_msg)


def check_raw_data(raw_data):
    """
        :Description:
            Raw data are expected to be of type byte array of length 12.

        :param raw_data: Raw data (received from external device).
        :type raw_data: bytearray

        :raises TypeError:
            Raw data are not a byte array.

        :raises ValueError:
            Raw data are not 12 bytes long.
    """
    try:
        if type(raw_data) != bytearray:
            raise TypeError
        if len(raw_data) != 12:
            raise ValueError
    except TypeError:
        error_msg = "Raw data are expected as bytearray"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "Raw data are expected to be 12 bytes long"
        logging.exception(error_msg)
        raise ValueError(error_msg)

def check_binary_can_data(binary_data):
    """
        :Description:
            Can data are expected as binary string of length 64 bits.

        :param binary_data: Binary data.
        :type binary_data: str

        :raises TypeError:
            Binary data are not a str.

        :raises ValueError:
            Binary data do not have size of 64 bits.
    """
    try:
        if type(binary_data) != str:
            raise TypeError
        if len(binary_data) != 64:
            raise ValueError
    except TypeError:
        error_msg = "Can binary data should be string"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "Can binary data must has 64 bits."
        logging.exception(error_msg)
        raise ValueError(error_msg)