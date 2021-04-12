import logging
from queue import Queue

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QPushButton, QLabel, QAction, QListWidget, QComboBox, QToolButton

from CanReader.Config.CanBus.CanConfigHandler import CanConfigHandler
from CanReader.GUI.CommunicationWindow.SerialSettings import SerialSettingWindow
from CanReader.GUI.CommunicationWindow.WifiSettings import WifiSettingWindow
from CanReader.GUI.ErrorTab.ErrorTab import ErrorTab
from CanReader.GUI.GraphTabs.GraphTab import GraphTab
from CanReader.GUI.OverviewTab.OverviewTab import OverviewTab
from CanReader.GUI.UpdateWindow.UpdateWindow import UpdateWindow
from CanReader.GUI.Help.AboutWindow.AboutDialog import AboutDialog
from CanReader.GUI.Help.Documentation.DocWindow import DocWindow


class MainWindow(QMainWindow):
    """
        :Inherit: :class:`QMainWindow`

        :Description:
            Main class of graphical part.\n
            Holds all other graphical widgets and communicate with them.\n
            UI was created in Qt Designer and loaded from "MainWindow.ui"
    """

    update_config_signal = QtCore.pyqtSignal()
    connection_request_signal = QtCore.pyqtSignal(str)
    disconnect_request_signal = QtCore.pyqtSignal()
    update_can_msg_signal = QtCore.pyqtSignal(str, str)
    update_connection_status_signal = QtCore.pyqtSignal(str)
    update_data_signal = QtCore.pyqtSignal(Queue)

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('GUI/MainWindow.ui', self)

        # Get dataConfig
        self.data_config_list = []
        self.set_data_config_list()

        self.action_save = self.findChild(QAction, "action_save")
        self.action_about = self.findChild(QAction, "action_about")
        self.action_documentation = self.findChild(QAction, "action_documentation")

        # help connections
        self.action_about.triggered.connect(self.open_about_dialog)
        self.action_documentation.triggered.connect(self.open_documentation_window)

        # testCommunication interface
        self.button_com = self.findChild(QPushButton, "button_connect")
        self.button_com.clicked.connect(self.send_com_request)

        self.button_com_setting = self.findChild(QToolButton, "toolbtn_com_settings")
        self.button_com_setting.clicked.connect(self.open_com_setting_window)

        self.com_status = self.findChild(QLabel, "label_status")
        self.update_connection_status_signal.connect(self.update_connection_status)

        self.cbox_com_type = self.findChild(QComboBox, "cbox_com_type")

        self.can_msg = self.findChild(QLabel, "label_can_msg")
        self.update_can_msg_signal.connect(self.update_can_msg)

        # Can variable interface
        self.button_update = self.findChild(QPushButton, "button_update")
        self.button_update.clicked.connect(self.open_update_window)

        self.variable_list = self.findChild(QListWidget, "variable_list_widget")
        self.variable_list.itemDoubleClicked.connect(self.open_update_window)
        self.variable_id_list = []

        #Create tabs
        self.tab_dict = {
            "overview_tab": OverviewTab(),
            "intake_tab": GraphTab(1),
            "engine_tab": GraphTab(2),
            "exhaust_tab": GraphTab(3),
            "fluid_tab": GraphTab(4),
            "suspension_tab": GraphTab(5),
            "acc_gyro_tab": GraphTab(6),
            "error_tab": ErrorTab(7)
         }
        self.tab_list = list(self.tab_dict.values())

        #Load tab widget add fill it with tabs
        self.tab_widget = self.findChild(QTabWidget, "tabWidget")
        self.tab_widget.addTab(self.tab_dict["overview_tab"], "General")
        self.tab_widget.addTab(self.tab_dict["intake_tab"], "Intake")
        self.tab_widget.addTab(self.tab_dict["engine_tab"], "Engine")
        self.tab_widget.addTab(self.tab_dict["exhaust_tab"], "Exhaust")
        self.tab_widget.addTab(self.tab_dict["fluid_tab"], "Fluid")
        self.tab_widget.addTab(self.tab_dict["suspension_tab"], "Suspension")
        self.tab_widget.addTab(self.tab_dict["acc_gyro_tab"], "Acc/Gyro")
        self.tab_widget.addTab(self.tab_dict["error_tab"], "Error")

        self.tab_widget.currentChanged.connect(self.show_variable_list_used_in_current_tab)
        self.tab_widget.currentChanged.connect(self.activate_current_tab)
        self.show_variable_list_used_in_current_tab()

        #fill tabs with variable configs and generate proper UI
        self.fill_tabs_with_variables()
        self.let_tabs_generate_graphics()

        self.update_data_signal.connect(self.push_data_to_tabs)

        self.show()

    def fill_tabs_with_variables(self):
        """
             :Description:
                This method is called only once when initializing.\n
                Append appropriate variable configuration for each tab.\n
                Based on given config graphics is generated and values are updated.
        """
        for config in self.data_config_list:
            group_id = config.group_id
            overview_id = config.overview_id
            if group_id < (self.tab_widget.count()) and group_id !=0:
                widget = self.tab_widget.widget(group_id)
                widget.add_config_variable(config)
            if overview_id > 0:
                widget = self.tab_widget.widget(0)
                widget.add_config_variable(config)

    def let_tabs_generate_graphics(self):
        """
            :Description:
                This method is called only once when initializing.\n
                Lets graph tabs and error tabs generate graphics based on configuration.
        """
        for tab_index in range(1, self.tab_widget.count()):
            tab = self.tab_widget.widget(tab_index)
            if type(tab) == GraphTab:
                tab.create_graphs()
            elif type(tab) == ErrorTab:
                tab.create_error_widgets()

        for tab_index in range(1, self.tab_widget.count()):
            tab = self.tab_widget.widget(tab_index)
            tab.sort_widget_list_by_id()

    def activate_current_tab(self):
        """
            :Description:
                Activate all widgets in selected graph tab.\n
                All other widget from graph tabs will be deactivated.\n
                Deactivated widget do not update values in graph, so app runs faster.
        """
        current_widget = self.tab_widget.currentWidget()
        for tab in self.tab_list:
            if type(tab) == GraphTab:
                if tab == current_widget:
                    tab.change_state(True)
                else:
                    tab.change_state(False)

    def show_variable_list_used_in_current_tab(self):
        """
            :Description:
                Update list of shown variable according to selected tab view(engine, suspension ,etc..)
        """
        current_widget = self.tab_widget.currentWidget()
        self.variable_list.clear()
        self.variable_id_list = []

        for config in self.data_config_list:
            if current_widget.group_id == 0:
                self.variable_list.addItem(config.name)
                self.variable_id_list.append(config.id)
                continue
            if config.group_id == current_widget.group_id:
                self.variable_list.addItem(config.name)
                self.variable_id_list.append(config.id)

    def push_data_to_tabs(self, queue):
        """
            :Description:
                Takes data received from formula and sends them to appropriate widget.

            :param queue: Queue of list of DataPoints containing decoded and processed data from formula
            :type queue: Queue(list[DataPoint])
        """
        if not queue.empty():
            data_list = queue.get()

            for data_point in data_list:
                try:
                    if data_point.overview_id != 0:
                        self.tab_list[0].update_data_signal.emit(data_point)

                    index = data_point.group_id
                    if index > len(self.tab_list):
                        raise ValueError

                    self.tab_list[index].update_data_signal.emit(data_point)
                except ValueError:
                    logging.warning("{} cannot be in group >= {}".format(data_point.name, len(self.tab_list)),
                                    exc_info=True)

    def send_com_request(self):
        """
            :Description:
                Send signal to start communication of specific type
        """
        if self.com_status.text() == "Offline":
            com_type = self.cbox_com_type.currentText()
            self.connection_request_signal.emit(com_type)
        else:
            self.disconnect_request_signal.emit()

    def open_com_setting_window(self):
        """
            :Description:
                Opens communication settings window.\n
                Based on user selection is opened either Serial config or Wi-Fi config.
        """
        com_type = self.cbox_com_type.currentText()
        if com_type.lower() == "wifi":
            self.com_setting_window = WifiSettingWindow(self)
        elif com_type.lower() == "serial":
            self.com_setting_window = SerialSettingWindow(self)

    def update_can_msg(self, can_id, can_msg):
        """
            :Description:
                Updates can message label in UI.

            :param can_id: Last received can id.
            :type can_id: str

            :param can_msg: Last received can message.
            :type can_msg: str
        """

        self.can_msg.setText(" ID:{} \t Data: {}".format(can_id, can_msg))

    def update_connection_status(self, status):
        """
            :Description:
                Show current connection status.\n
                Based on new status change button between "Connect" and "Disconnect".\n
                Status can be "Offline", "Connecting","Reconnecting", "Online"

            :param status: Connection status.
            :type status: str
        """
        if status != self.com_status.text():
            self.com_status.setText(status)
            if status == "Offline":
                self.button_com.setText("Connect")
            else:
                self.button_com.setText("Disconnect")

    def open_update_window(self):
        """
            :Description:
                This method is invoked when update button is clicked.\n
                Open update window, where user can adjust configuration for selected can variable.
        """
        selected_variable_position = self.variable_list.currentRow()
        if selected_variable_position != -1:
            self.update_win = UpdateWindow(self, self.variable_id_list[selected_variable_position])

    def set_data_config_list(self):
        """
            :Description:
                Loads current data configuration.
        """
        config = CanConfigHandler()
        self.data_config_list = config.load_from_config_file()

    def open_about_dialog(self):
        self.about_dialog = AboutDialog()

    def open_documentation_window(self):
        """
            :Description:
                Open documentation window.
        """
        self.documentation_win = DocWindow()
