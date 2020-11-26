from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from GUI.GraphTabs.Graph import Graph
from GUI.Tab import Tab

class GraphTab(Tab):

    def __init__(self, group_id):
        Tab.__init__(self, group_id)

    def create_graphs(self):
        for var in self.config_variable_list:
            name = var.name
            unit = var.unit
            id = var.widget_id
            self.widget_list.append(Graph(name, unit, id))

        self.add_graphs_to_layout()

    def change_state(self, state):
        for widget in self.widget_list:
            widget.state_signal.emit(state)

    def add_graphs_to_layout(self):
        layout = QVBoxLayout()
        for graph in self.widget_list:
            layout.addWidget(graph)

        self.setLayout(layout)