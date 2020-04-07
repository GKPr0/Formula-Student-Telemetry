"""
Main handler of project.

"""
import threading
import sys
from PyQt5 import QtWidgets, QtCore
from CanReader.Config.Config import Config
from CanReader.Communication.SocketClient import SocketClient
from CanReader.DataProcessing.RawData import RawData
from CanReader.DataProcessing.DataProcessing import DataProcessing
from CanReader.GUI.MainWindow import MainWindow
from CanReader.Logger.DataLogger import DataLogger
import time

class App:
    '''
        This is a main class of whole application.
        \n
        This class handle communication ,data processing and gui in separate threads.
        Main purpose of this class is to convey data from one thread to another one.
    '''

    config_file_name = "config_file.ini"
    IP = "192.168.1.100"
    PORT = 80

    def __init__(self):
        self.data_logger = DataLogger()
        self.update_config()

        self.socket_client = SocketClient(self.IP, self.PORT)

        self.data_to_display = None
        self.data_from_formula = None

        self.gui_ready = False

        self.communication = threading.Thread(target=self.run_communication, name='communication')
        self.gui = threading.Thread(target=self.run_gui, name='gui')

        self.communication.start()
        self.gui.start()

    def run_communication(self):
        '''
            This method runs in separate thread, that invoke communication with formula.
            Once data packet from formula arrived new thread will be created and communication will start over
            Thread created in this method will processed income data
        '''
        #self.socket_client.status_changed_signal.connect(self.main_window.update_status)
        self.socket_client.connect_to_server()
        while True:
            self.data_from_formula = self.socket_client.get_data()
            #self.data_from_formula = "ID600XAB0000000BFFCFF"
            #self.push_to_data_logger()
            self.run_data_processing()


    def run_data_processing(self):
        """
            This method is called in temporary thread invoked by communication thread.
            Result is decoded and processed data packet prepared to be display in gui.
        """

        raw_data = RawData(self.data_from_formula)
        can_id, can_data = raw_data.split_data()
        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        self.data_to_display = data_decoder.data_decode()
        self.update_gui()


    def run_gui(self):
        """
            This method runs in separate thread, that take cares of data visualization and interaction with user.
        """
        gui = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow()

        self.main_window.update_config_signal.connect(self.update_config)
        self.main_window.action_save.triggered.connect(self.data_logger.save_raw_can)

        self.gui_ready = True
        sys.exit(gui.exec_())


    def update_gui(self):
        """
            This method is called by gui to update it self´s data
        """
        if self.gui_ready:
            self.gui_ready = False
            self.main_window.push_data_to_tabs(self.data_to_display)
            self.main_window.update_can_msg(self.data_from_formula)
            self.main_window.update_status(self.socket_client.status)
            self.gui_ready = True

    def update_config(self):
        """
            This method is called either at booting app or whenever data config is changed.
        """
        config = Config()
        self.data_config_list = config.load_from_config_file()

    def push_to_data_logger(self):
        self.data_logger.get_raw_can(self.data_from_formula)

    def close_app(self):
        quit()
        print("test")


if __name__ == "__main__":
    app = App()
