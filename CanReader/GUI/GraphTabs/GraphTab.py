from PyQt5.QtWidgets import QVBoxLayout

from CanReader.GUI.GraphTabs.Graph import Graph
from CanReader.GUI.Tab import Tab


class GraphTab(Tab):
    """
        :Inherit: :class:`Tab`

        :Description:
            Graph tab is used to create and handle graphs\n
            For more info see :class:`Graph`.

        :param group_id: Group id based on which the configuration is assigned.
        :type group_id: int
    """

    def __init__(self, group_id):
        Tab.__init__(self, group_id)

    def create_graphs(self):
        """
            :Description:
                Create Graph widgets based on configuration.
        """
        for var in self.config_variable_list:
            name = var.name
            unit = var.unit
            id = var.widget_id
            self.widget_list.append(Graph(name, unit, id))

        self.add_graphs_to_layout()

    def change_state(self, state):
        """
            :Description:
                Send state signal to all containing graph.\n
                The status signal lets the graphs know if they should be plotted or not.

            :param state:
            :type state: bool
        """
        for widget in self.widget_list:
            widget.state_signal.emit(state)

    def add_graphs_to_layout(self):
        """
            :Description:
                Add Graphs widget to layout.
        """
        layout = QVBoxLayout()
        for graph in self.widget_list:
            layout.addWidget(graph)

        self.setLayout(layout)