import logging

from PyQt5 import uic
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QRadioButton

from CanReader.Config.CanBus.CanConfigHandler import CanConfigHandler
from CanReader.Config.CanBus.CanDataConfig import CanDataConfig
from CanReader.GUI.UpdateWindow.WarningWindow import WarningWindow


class UpdateWindow(QMainWindow):
    """
        :Inherit: :class:`QMainWindow`

        :Description:
            Graphical interface to update variable configuration.\n
            User can changed can id, start bit, length, multiplier and offset.
            UI was created in Qt Designer and loaded from "UpdateWindow.ui"

        :param main_window: Main app window object is load because of accessibility of signal.
        :type main_window: MainWindow

        :param config_id: Id of variable which configs user want to adjust.
        :type config_id: int

        :raises TypeError:
            Config_id is not an integer

        :raises ValueError:
            Config_id is greater then maximal id in config file

        .. note::
            Change signal/slot logic. Takes main app object as parameter to send its signal isn´t best approach.
    """

    def __init__(self, main_window, config_id):
        QMainWindow.__init__(self)
        uic.loadUi('GUI/UpdateWindow/UpdateWindow.ui', self)
        self.main_window = main_window

        # Check config_id
        CanConfigHandler.check_config_id(config_id)

        # Get current data
        self.config = CanConfigHandler()
        self.config_id = config_id
        self.data_config = self.config.load_selected_from_config_file(self.config_id)

        self.setup_dynamic_title()

        self.update_button = self.findChild(QPushButton, "save_button")
        self.update_button.clicked.connect(self.update_config)

        # Load radio buttons
        self.little_endian = self.findChild(QRadioButton, "little_endian")
        self.big_endian = self.findChild(QRadioButton, "big_endian")
        self.little_endian.clicked.connect(self.is_little_endian_possible)

        # Load textbox from gui
        self.name_input = self.findChild(QLineEdit, "name_input")
        self.id_input = self.findChild(QLineEdit, "id_input")
        self.start_bit_input = self.findChild(QLineEdit, "start_bit_input")
        self.length_input = self.findChild(QLineEdit, "length_input")
        self.length_input.editingFinished.connect(self.is_little_endian_possible)
        self.multiplier_input = self.findChild(QLineEdit, "multiplier_input")
        self.offset_input = self.findChild(QLineEdit, "offset_input")
        self.unit_input = self.findChild(QLineEdit, "unit_input")

        self.name_input.textChanged.connect(self.setup_dynamic_name_box_width)

        # Load current data to textBoxes
        self.show_data()

        self.show()

    def show_data(self):
        """
            :Description:
                Loads config for selected variable and displays it.
        """
        self.name_input.setText(str(self.data_config.name))
        self.id_input.setText(str(self.data_config.can_id))
        self.start_bit_input.setText(str(self.data_config.start_bit))
        self.length_input.setText(str(self.data_config.length))
        self.multiplier_input.setText(str(self.data_config.multiplier))
        self.offset_input.setText(str(self.data_config.offset))
        self.unit_input.setText(str(self.data_config.unit))

        if self.is_little_endian_possible():
            if str(self.data_config.endian) == "L":
                self.little_endian.setChecked(True)
                return

        self.big_endian.setChecked(True)

    def update_config(self):
        """
            :Description:
                Takes new data given by user and use them to update configuration file.\n
                New DataConfig object will be temporary created because it will automatically check
                validity of input parameters.\n
                Once config is updated, config update signal is emitted.
        """
        id = self.config_id
        group_id = self.data_config.group_id
        widget_id = self.data_config.widget_id
        overview_id = self.data_config.overview_id
        name = self.name_input.text()
        unit = self.unit_input.text()
        can_id = self.id_input.text()
        start_bit = self.start_bit_input.text()
        length = self.length_input.text()
        multiplier = self.multiplier_input.text()
        offset = self.offset_input.text()

        if self.little_endian.isChecked():
            endian = "L"
        elif self.big_endian.isChecked():
            endian = "B"
        else:
            endian = ""

        warning_window = WarningWindow(can_id, start_bit, length, multiplier, offset, endian)

        if warning_window.check_user_inputs():

            new_data_config = CanDataConfig(int(id), int(group_id), int(widget_id), int(overview_id), str(name), str(unit), str(can_id), int(start_bit),
                                            int(length), float(multiplier), float(offset), str(endian))

            self.config.update_section_in_config(new_data_config)

            self.main_window.update_config_signal.emit()

            self.close()

    def is_little_endian_possible(self):
        """
            :Description:
                Set checkability of little endian.\n
                Little endian cannot be set if data length is divisible by 8 WITH remainder
                and if data length is less or eq 8.\n

            :return: True if little endian can be set.
            :rtype: bool

        """
        if int(self.length_input.text()) % 8 != 0 or int(self.length_input.text()) <= 8:
            if self.little_endian.isChecked():
                self.big_endian.setChecked(True)
                self.little_endian.setCheckable(False)
                return False
        else:
            self.little_endian.setCheckable(True)
            return True

    def setup_dynamic_title(self):
        """
            :Description:
                Set window title based on data config name.
        """
        name = str(self.data_config.name)

        if name != "":
            self.setWindowTitle("Update {} properties".format(name))
        else:
            self.setWindowTitle("Update CAN BUS variable")

    def setup_dynamic_name_box_width(self):
        """
            :Description:
                Adjust name box size if name is too long.
        """
        text = self.name_input.text()
        size = self.name_input.size()

        font = self.name_input.font()
        fm = QFontMetrics(font)
        pixel_width = fm.width(text)

        if pixel_width > size.width():
            self.name_input.setFixedSize((pixel_width + 20), size.height())
