import math

from PyQt5.QtWidgets import QGridLayout

from CanReader.GUI.ErrorTab.ErrorWidget import ErrorWidget
from CanReader.GUI.Tab import Tab


class ErrorTab(Tab):

    def __init__(self, group_id):
        Tab.__init__(self, group_id)

        self.max_row = 0
        self.max_col = 0

    def create_error_widgets(self):
        for var in self.config_variable_list:
            name = var.name
            id = var.widget_id
            self.widget_list.append(ErrorWidget(name, id))

        self.add_error_widget_to_layout()

    def add_error_widget_to_layout(self):
        self.count_grid_size()

        layout = QGridLayout()
        col = 0
        row = 0
        for err_widget in self.widget_list:
            layout.addWidget(err_widget, row, col)
            col += 1
            if col >= self.max_col:
                row += 1
                col = 0

        self.setLayout(layout)

    def count_grid_size(self):
        count = len(self.widget_list)

        sqrt = math.ceil(math.sqrt(count))
        if math.pow(sqrt, 2) == count:
            self.max_col = sqrt
            self.max_row = sqrt
        else:
            self.max_col = sqrt
            self.max_row = sqrt - 1
