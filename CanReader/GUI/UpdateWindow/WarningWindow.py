from PyQt5.QtWidgets import QMessageBox


class WarningWindow:
    """
        This Class is used to check user parameters given in UpdateWindow

        :param can_id:
        :type can_id: int
        :param start_bit:
        :type start_bit: int
        :param length:
        :type length: int
        :param multiplier:
        :type multiplier: float / int
        :param offset:
        :type offset: float / int
    """

    def __init__(self, can_id, start_bit, length, multiplier, offset, endian):

        self.can_id = can_id
        self.start_bit = start_bit
        self.length = length
        self.multiplier = multiplier
        self.offset = offset
        self.endian = endian

    def check_user_inputs(self):
        """
        This method runs series of check method.
        These methods check if input parameters given this class are valid.

        :return: True if all checked parameters are valid.
        :rtype: bool
        """
        if not self.check_can_id():
            return False
        if not self.check_start_bit():
            return False
        if not self.check_length():
            return False
        if not self.check_multiplier():
            return False
        if not self.check_offset():
            return False
        if not self.check_endian():
            return False
        return True

    @staticmethod
    def show_warning_window(title, msg):
        """
            This method will display message box with given title and message

            :param title: Title of message box
            :param title: str
            :param msg: Message that will be displayed
            :type msg: str
        """
        warningwindow = QMessageBox()
        warningwindow.setIcon(QMessageBox.Warning)
        warningwindow.setWindowTitle(title)
        warningwindow.setText(msg)
        warningwindow.setStandardButtons(QMessageBox.Ok)
        warningwindow.exec_()

    def check_can_id(self):
        """
            Check validity of can id
        """
        try:
            if int(self.can_id) < 0 or int(self.can_id) > 999:
                raise ArithmeticError
            return True
        except ValueError:
            self.show_warning_window("Can ID Error", "Can ID must be an integer")
            return False
        except ArithmeticError:
            self.show_warning_window("Can ID Error", "Can ID must be in range 0 - 999")
            return False

    def check_start_bit(self):
        """
            Check validity of star bit
        """
        try:
            if int(self.start_bit) < 0 or int(self.start_bit) > 63:
                raise ArithmeticError
            return True
        except ValueError:
            self.show_warning_window("Start bit Error", "Start bit must be an integer")
            return False
        except ArithmeticError:
            self.show_warning_window("Start bit Error", "Start bit must be in range 0 - 63")
            return False

    def check_length(self):
        """
            Check validity of length
        """
        try:
            if int(self.length) < 1 or int(self.length) > 63:
                raise ArithmeticError
            return True
        except ValueError:
            self.show_warning_window("Length Error", "Length must be an integer")
            return False
        except ArithmeticError:
            self.show_warning_window("Length Error", "Length must be in range 1 - 63")
            return False

    def check_multiplier(self):
        """
            Check validity of multiplier
        """
        try:
            if float(self.multiplier) == 0:
                raise ArithmeticError
            return True
        except ValueError:
            self.show_warning_window("Multiplier Error", "Multiplier must be an integer or float")
            return False
        except ArithmeticError:
            self.show_warning_window("Multiplier Error", "Multiplier cannot be 0")
            return False

    def check_offset(self):
        """
            Check validity of offset
        """
        try:
            float(self.offset)
            return True
        except ValueError:
            self.show_warning_window("Offset Error", "Offset must be an integer or float")
            return False

    def check_endian(self):
        """
            Endian expected as "L" or "B" of type str
        """
        try:
            if type(self.endian) != str:
                raise TypeError
            if self.endian not in ["L", "B"]:
                raise ValueError
            return True
        except TypeError:
            self.show_warning_window("Endian Error", "Endian must be string")
            return False
        except ValueError:
            self.show_warning_window("Endian Error", "Endian is expected as 'L' or 'B'")
            return False
