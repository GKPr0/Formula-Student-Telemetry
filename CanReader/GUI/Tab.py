from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from CanReader.GUI.GraphTabs.Graph import Graph

class Tab(QWidget):

    def __init__(self, group_id = 0):
        QWidget.__init__(self)

        self.group_id = group_id
        self.config_variable_list = []
        self.widget_list = []

    def tab_info(self):
        for var in self.config_variable_list:
            print(var)

    def add_config_variable(self, variable):
        self.config_variable_list.append(variable)

    def update_data(self, data_point):
        for widget in self.widget_list:
            if widget.id == data_point.id:
                widget.update_data(data_point.value)

