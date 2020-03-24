from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,  QPushButton, QLineEdit

from CanReader.Config.Config import Config
from CanReader.Config.DataConfig import DataConfig
from CanReader.GUI.UpdateWindow.WarningWindow import WarningWindow


class UpdateWindow(QMainWindow):
    """
        This class takes care about updating of configuration file.
        User can changed can id, start bit, length, multiplier and offset.

        Works with data in format DataConfig

        :param main_window: This is load because of accessibility of signal, that will be emitted
        :type main_window: MainWindow
        :param config_id: unique id of clicked variable. Used to load DataConfig on this id
        :type config_id: int

        :raises TypeError: config_id is not an integer

        :raises ValueError: config_id is greater then maximal id in config file

    """

    def __init__(self, main_window, config_id):
        QMainWindow.__init__(self)
        uic.loadUi('CanReader/GUI/UpdateWindow/UpdateWindow.ui', self)
        self.main_window = main_window

        # Check config_id
        self.check_config_id(config_id)

        # Get current data
        self.config = Config()
        self.config_id = config_id
        self.data_config = self.config.load_selected_from_config_file(self.config_id)

        self.setWindowTitle("Update your Variable")
        self.update_button = self.findChild(QPushButton, "save_button")
        self.update_button.clicked.connect(self.update_config)

        # Load textbox from gui
        self.name_input = self.findChild(QLineEdit, "name_input")
        self.id_input = self.findChild(QLineEdit, "id_input")
        self.start_bit_input = self.findChild(QLineEdit, "start_bit_input")
        self.length_input = self.findChild(QLineEdit, "length_input")
        self.multiplier_input = self.findChild(QLineEdit, "multiplier_input")
        self.offset_input = self.findChild(QLineEdit, "offset_input")
        self.unit_input = self.findChild(QLineEdit, "unit_input")

        # Load current data to textBoxes
        self.show_data()

        self.show()

    def show_data(self):
        """
            This method takes current data from selected variable and display them
        """
        self.name_input.setText(str(self.data_config.name))
        self.id_input.setText(str(self.data_config.can_id))
        self.start_bit_input.setText(str(self.data_config.start_bit))
        self.length_input.setText(str(self.data_config.length))
        self.multiplier_input.setText(str(self.data_config.multiplier))
        self.offset_input.setText(str(self.data_config.offset))
        self.unit_input.setText(str(self.data_config.unit))

    def update_config(self):
        """
            This method will take new data given by user and use them to update configuration file
            New DataConfig object will be temporary created because it will automatically check
            validity of input parameters.
            Once config is updated signal for config update is emitted and received by main object App
        """
        id = self.config_id
        group_id = self.data_config.group_id
        widget_id = self.data_config.widget_id
        name = self.name_input.text()
        unit = self.unit_input.text()
        can_id = self.id_input.text()
        start_bit = self.start_bit_input.text()
        length = self.length_input.text()
        multiplier = self.multiplier_input.text()
        offset = self.offset_input.text()

        warning_window = WarningWindow(can_id, start_bit, length, multiplier, offset)

        if warning_window.check_user_inputs():

            new_data_config = DataConfig(int(id), int(group_id), int(widget_id), str(name), str(unit), int(can_id), int(start_bit),
                                         int(length), float(multiplier), float(offset))

            self.config.update_section_in_config(new_data_config)

            self.main_window.update_config_signal.emit()

            self.close()

    @staticmethod
    def check_config_id(config_id):
        """
            This method check if input parametr config ID is in right format.
            Config ID has to be integer in range of [0, number of data configs]
        """
        try:
            if type(config_id) != int:
                raise TypeError
            if config_id < 0 or config_id > Config().number_of_data_configs:
                raise ValueError
        except TypeError:
            raise TypeError("Config id must be integer")
        except ValueError:
            raise ValueError("Config id must be in range of data config in config file {}".format(Config().number_of_data_configs))
