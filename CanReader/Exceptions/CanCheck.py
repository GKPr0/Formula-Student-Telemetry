import logging


def check_id(id):
    """
        Check validity of ID.
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
        Check validity of group id
    """
    try:
        if group_id < 0 or group_id > 999:
            raise ValueError
        if type(group_id) != int:
            raise TypeError
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
        Check validity of widget id
    """
    try:
        if widget_id < 0 or widget_id > 50:
            raise ValueError
        if type(widget_id) != int:
            raise TypeError
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
        Check if can id is valid. Expected HEX string of len 3
    """
    try:
        if type(can_id) != str:
            raise TypeError
        int(can_id, 16)
        if len(can_id) > 3:
            raise ValueError
    except TypeError:
        error_msg = "Can ID must be a hex string"
        logging.exception(error_msg)
        raise TypeError(error_msg)
    except ValueError:
        error_msg = "CAN ID must be hex of max length 3"
        logging.exception(error_msg)
        raise ValueError(error_msg)


def check_name(name):
    """
        Check validity of name
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
        Check validity of unit
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
        Check validity of star bit
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
        Check validity of length
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
        Check validity of multiplier
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
        Check validity of offset
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
        Endian expected as "L" or "B" of type str
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
        Check validity of value. Expected to be float or int
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
        Check validity of raw_data type. Expected byte array
    """
    try:
        if type(raw_data) != bytearray:
            raise TypeError

    except TypeError:
        error_msg = "Raw data are expected as bytearray"
        logging.exception(error_msg)
        raise TypeError(error_msg)

def check_binary_can_data(binary_data):
    """
        Check validity of can data in binary. Expected string of 64 bits
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