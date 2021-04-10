from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget


class Tab(QWidget):
    """
        :Inherit: :class:`QWidget`

        :Description:
            Base class for all types of tabs ie. GraphTab, ErrorTab, OverviewTab.\n
            Implement basic methods for loading config and updating values of variables.

        :param group_id: Group id based on which the configuration is assigned.
        :type group_id: int, optional
    """
    update_data_signal = QtCore.pyqtSignal(object)

    def __init__(self, group_id=0):
        QWidget.__init__(self)

        self.group_id = group_id
        self.config_variable_list = []
        self.widget_list = []
        self.update_data_signal.connect(self.update_data)

    def tab_info(self):
        """
            :Description:
                Print info about every assigned variable.
        """
        for var in self.config_variable_list:
            print(var)

    def add_config_variable(self, variable):
        """
            :Description:
                Append new variable config to config list.

            :param variable: Variable config.
            :type variable: CanDataConfig
        """
        self.config_variable_list.append(variable)

    def update_data(self, data_point):
        """
            :Description:
                Update data in proper widget.

            :param data_point: Data container
            :type data_point: DataPoint
        """
        widget = self.widget_list[data_point.id]
        widget.update_signal.emit(data_point.value)

    def sort_widget_list_by_id(self):
        """
            :Description:
                Sort generated widgets by its id, so data can be passed directly without need looping over all widgets.
        """
        self.widget_list.sort(key=lambda x: x.id, reverse=False)
