from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout
from CanReader.GUI.GraphTabs.Graph import Graph
from CanReader.GUI.Tab import Tab
from CanReader.GUI.ErrorTab.ErrorWidget import ErrorWidget

import math

class ErrorTab(Tab):

    def __init__(self, group_id):
        Tab.__init__(self, group_id)

        self.error_widget_list = []
        self.max_row = 0
        self.max_col = 0

    def create_error_widgets(self):
        for var in self.config_variable_list:
            name = var.name
            self.error_widget_list.append(ErrorWidget(name))

        self.add_error_widget_to_layout()

    def add_error_widget_to_layout(self):
        self.count_grid_size()

        layout = QGridLayout()
        col = 0
        row = 0
        for err_widget in self.error_widget_list:
            layout.addWidget(err_widget, row, col)
            col += 1
            if col >= self.max_col:
                row += 1
                col = 0

        self.setLayout(layout)

    def count_grid_size(self):
        count = len(self.error_widget_list)

        sqrt = math.ceil(math.sqrt(count))
        if math.pow(sqrt, 2) == count:
            self.max_col = sqrt
            self.max_row = sqrt
        else:
            self.max_col = sqrt
            self.max_row = sqrt - 1
