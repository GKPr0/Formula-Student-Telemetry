from PyQt5 import uic, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from GUI.GraphTabs.Graph import Graph
import threading

class Tab(QWidget, QThread):

    update_data_signal = QtCore.pyqtSignal(object)

    def __init__(self, group_id = 0):
        QWidget.__init__(self)
        QThread.__init__(self)

        self.group_id = group_id
        self.config_variable_list = []
        self.widget_list = []
        self.update_data_signal.connect(self.update_data)

        self.start()

    def tab_info(self):
        for var in self.config_variable_list:
            print(var)

    def add_config_variable(self, variable):
        self.config_variable_list.append(variable)

    def update_data(self, data_point):
        widget = self.widget_list[data_point.id]
        widget.update_signal.emit(data_point.value)

    def sort_widget_list_by_id(self):
        self.widget_list.sort(key=lambda x: x.id, reverse=False)

