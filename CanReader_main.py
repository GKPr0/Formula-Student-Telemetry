"""
Main handler of project.

"""
import threading
import sys
from PyQt5 import QtWidgets, QtCore
from CanReader.Config.Config import Config
from CanReader.Communication.SocketServer import SocketServer
from CanReader.DataProcessing.RawData import RawData
from CanReader.DataProcessing.DataProcessing import DataProcessing
from CanReader.GUI.MainWindow import MainWindow
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
    PORT = 32001

    def __init__(self):
        self.update_config()
        #self.socket_server = SocketServer(self.IP, self.PORT)

        self.data_to_display = None
        self.data_from_formula = None
        self.communication_status = "Offline"

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
        while True:
            # self.data_from_formula = self.socket_server.get_data()
            self.data_from_formula = "ID100XAB000800B00C00"
            data_processing = threading.Thread(target=self.run_data_processing, name='data_processing')
            data_processing.start()

    def run_data_processing(self):
        """
            This method is called in temporary thread invoked by communication thread.
            Result is decoded and processed data packet prepared to be display in gui.
        """

        raw_data = RawData(self.data_from_formula)
        can_id, can_data = raw_data.split_data()
        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        self.data_to_display = data_decoder.data_decode()
        #print(self.data_from_formula)
        #print(self.data_to_display)

    def run_gui(self):
        """
            This method runs in separate thread, that take cares of data visualization and interaction with user.
            Part of this method is timer that calls method for data update every 100ms
        """
        gui = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow()

        self.main_window.update_config_signal.connect(self.update_config)

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_gui)
        timer.start(100)

        sys.exit(gui.exec_())

    def update_gui(self):
        """
            This method is called by gui to update it self´s data
        """
        self.main_window.update_labels(self.data_to_display)
        self.main_window.update_can_msg(self.data_from_formula)
        self.main_window.update_status(self.communication_status)

    def update_config(self):
        """
            This method is called either at booting app or whenever data config is changed.
        """
        config = Config()
        self.data_config_list = config.load_from_config_file()


if __name__ == "__main__":
    app = App()
