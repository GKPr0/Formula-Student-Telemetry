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
import queue
import sys

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

        self.data_queue = queue.Queue(maxsize= 25)
        self.gui_ready = False

        self.gui = threading.Thread(target=self.run_gui, name='gui')
        self.communication = threading.Thread(target=self.run_communication, name='communication')
        self.gui.start()



    def run_communication(self):
        '''
            This method runs in separate thread, that invoke communication with formula.
            Once data packet from formula arrived new thread will be created and communication will start over
            Thread created in this method will processed income data
        '''
        # Whenever connection status changed signal to gui will be send
        self.socket_client.status_changed.connect(self.main_window.update_connection_status_signal.emit)
        # Client setup -> try to connect to a server
        self.socket_client.connect_to_server()
        i = 0
        while True:
            data_from_formula = self.socket_client.get_data()
            print(data_from_formula)
            #data_from_formula = ["ID600X00A5FFFFBFFCFF", "ID600X00B8FFFFBFFCFF", "ID600X00CACFFFFBFFCFF", "ID600X00D8FFFFBFFCFF"]

            # Update Can msg shown in gui
            self.main_window.update_can_msg_signal.emit(data_from_formula)

            # Create threads that run in parallel.
            data_processing_thread = threading.Thread(target=self.run_data_processing, name='data_processing',
                                                      args=(data_from_formula,))
            data_logging_thread = threading.Thread(target=self.push_to_data_logger, name='data_logging',
                                                   args=(data_from_formula,))
            data_processing_thread.start()
            data_logging_thread.start()
            # Wait for both threads to be done.
            data_processing_thread.join()
            data_logging_thread.join()

            #i += 1
            #if i > 3:
            #    i = 0


    def run_data_processing(self, data_from_formula):
        """
            This method is called in temporary thread invoked by communication thread.
            Result is decoded and processed data packet prepared to be display in gui.
        """

        raw_data = RawData(data_from_formula)
        can_id, can_data = raw_data.split_data()

        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        data_to_display = data_decoder.data_decode()
        #if can_id == str(556):
        #    print(can_id)
        #    print(can_data)
        #    print(data_to_display)
        self.data_queue.put(data_to_display)

    def run_gui(self):
        """
            This method runs in separate thread, that take cares of data visualization and interaction with user.
        """
        gui = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow()

        self.main_window.update_config_signal.connect(self.update_config)
        self.main_window.action_save.triggered.connect(self.data_logger.set_save_path)

        self.gui_ready = True
        self.communication.start()

        timer = QtCore.QTimer()

        timer.start(33)
        timer.timeout.connect(self.update_gui)

        sys.exit(gui.exec_())

    def update_config(self):
        """
            This method is called either at booting app or whenever data config is changed.
        """
        config = Config()
        self.data_config_list = config.load_from_config_file()

    def update_gui(self):
        self.main_window.update_data_signal.emit(self.data_queue)

    def push_to_data_logger(self, data_from_formula):
        self.data_logger.get_raw_can(data_from_formula)


if __name__ == "__main__":
    app = App()
