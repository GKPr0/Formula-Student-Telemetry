from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QPushButton, QLabel, QAction, QListWidget

from CanReader.GUI.UpdateWindow.UpdateWindow import UpdateWindow
from CanReader.GUI.OverviewTab.OverviewTab import OverviewTab
from CanReader.GUI.GraphTabs.GraphTab import GraphTab
from CanReader.GUI.ErrorTab.ErrorTab import ErrorTab
from CanReader.Config.Config import Config

class MainWindow(QMainWindow):
    """
        Main class of graphical part.
         Contains all other graphical widget and send data to them
    """

    update_config_signal = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('CanReader/GUI/MainWindow.ui', self)

        # Get dataConfig
        self.data_config_list = []
        self.set_data_config_list()

        self.action_save = self.findChild(QAction, "action_save")

        self.can_msg = self.findChild(QLabel, "label_can_msg")
        self.status = self.findChild(QLabel, "label_status")

        self.button_update = self.findChild(QPushButton, "button_update")
        self.button_update.clicked.connect(self.open_update_window)

        self.variable_list = self.findChild(QListWidget, "variable_list_widget")
        self.variable_id_list = []

        #Create tabs
        self.tab_list = {
            "overview_tab": OverviewTab(),
            "intake_tab": GraphTab(1),
            "engine_tab" : GraphTab(2),
            "exhaust_tab" : GraphTab(3),
            "fluid_tab" : GraphTab(4),
            "suspension_tab" : GraphTab(5),
            "acc_gyro_tab" : GraphTab(6),
            "error_tab" : ErrorTab(7)
         }

        #Load tab widget add fill it with tabs
        self.tab_widget = self.findChild(QTabWidget, "tabWidget")
        self.tab_widget.addTab(self.tab_list["overview_tab"], "General")
        self.tab_widget.addTab(self.tab_list["intake_tab"], "Intake")
        self.tab_widget.addTab(self.tab_list["engine_tab"], "Engine")
        self.tab_widget.addTab(self.tab_list["exhaust_tab"], "Exhaust")
        self.tab_widget.addTab(self.tab_list["fluid_tab"], "Fluid")
        self.tab_widget.addTab(self.tab_list["suspension_tab"], "Suspension")
        self.tab_widget.addTab(self.tab_list["acc_gyro_tab"], "Acc/Gyro")
        self.tab_widget.addTab(self.tab_list["error_tab"], "Error")

        self.tab_widget.currentChanged.connect(self.show_variable_list_used_in_current_tab)
        self.show_variable_list_used_in_current_tab()

        #fill tabs with variable configs and generate proper UI
        self.fill_tabs_with_variables()
        self.let_tabs_generate_graphics()

        self.show()

    def fill_tabs_with_variables(self):
        for config in self.data_config_list:
            group_id = config.group_id
            if group_id < (self.tab_widget.count()):
                widget = self.tab_widget.widget(group_id)
                widget.add_config_variable(config)

    def let_tabs_generate_graphics(self):
        for tab_index in range(1, self.tab_widget.count()):
            widget = self.tab_widget.widget(tab_index)
            if type(widget) == GraphTab:
                widget.create_graphs()
            elif type(widget) == ErrorTab:
                widget.create_error_widgets()

    def show_variable_list_used_in_current_tab(self):
        """
            This method update shown variable according to selected tab view(engine, suspension ,etc..)
        """
        current_widget = self.tab_widget.currentWidget()
        self.variable_list.clear()
        self.variable_id_list = []

        for config in self.data_config_list:
            if config.group_id == current_widget.group_id:
                self.variable_list.addItem(config.name)
                self.variable_id_list.append(config.id)


    def push_data_to_tabs(self, data_list):
        """
            This method takes data received from formula and sends them to place where will be displayed
            :param data_list: list of DataPoints containing decoded and processed data from formula
            :type data_list: DataPoint
        """
        for tab in self.tab_list.values():
            for data_point in data_list:
                if tab.group_id == data_point.group_id:
                    tab.update_data(data_point)

    def update_can_msg(self, can_msg):
        """
            This method update can message label in gui
            :param can_msg: last received can message
        """
        self.can_msg.setText(str(can_msg))


    def update_status(self, status):
        """
            This method update connection status between app and formula
            :param status: Status can be "Offline" , "Online" , "Connecting"
        """
        if status != self.status.text():
            self.status.setText(status)


    def open_update_window(self):
        """
            This method is invoked when update button is clicked.
            Open update window, where user can adjust configuration for selected variable
        """
        selected_variable_position = self.variable_list.currentRow()
        if selected_variable_position != -1:
            self.update_win = UpdateWindow(self, self.variable_id_list[selected_variable_position])

    def set_data_config_list(self):
        """
            This method load current data configuration
        """
        config = Config()
        self.data_config_list = config.load_from_config_file()
