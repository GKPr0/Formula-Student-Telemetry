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

        self.data_queue = queue.Queue(maxsize=25)

        self.gui_ready = False

        self.gui = threading.Thread(target=self.run_gui, name='gui')
        self.communication = threading.Thread(target=self.run_communication, name='communication')
        self.gui.start()

    def run_communication(self):
        '''
        Runs in separate thread, that invoke communication with formula.
        Once data packet from formula arrived new data processing thread will be created and
        communication will start over.
        '''
        # Whenever connection status changed signal to gui will be send
        self.socket_client.status_changed.connect(self.main_window.update_connection_status_signal.emit)
        # Client setup -> try to connect to a server
        self.socket_client.connect_to_server()
        while True:
            data_from_formula = self.socket_client.get_data()

            data_processing_thread = threading.Thread(target=self.run_data_processing, name='data_processing',
                                                      args=(data_from_formula,))
            data_processing_thread.start()
            time.sleep(0.01)

    def run_data_processing(self, data_from_formula):
        """
            Called in temporary thread invoked by communication thread.
            Result is decoded and processed data packet prepared to be display in gui.
        """

        raw_data = RawData(data_from_formula)
        can_id, can_data = raw_data.split_data()
        print(can_data)
        data_logging_thread = threading.Thread(target=self.push_to_data_logger, name='data_logging',
                                               args=(can_id, can_data))
        data_logging_thread.start()

        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        data_to_display = data_decoder.data_decode()

        self.data_queue.put(data_to_display)

        data_logging_thread.join()

    def run_gui(self):
        """
            This method runs in separate thread, that take cares of data visualization and interaction with user.
        """
        gui = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow()

        self.main_window.update_config_signal.connect(self.update_config)
        self.main_window.action_save.triggered.connect(self.data_logger.set_save_path)
        gui.aboutToQuit.connect(self.on_app_exit)

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

    def push_to_data_logger(self, can_id, can_data):
        # Update Can msg shown in gui
        self.main_window.update_can_msg_signal.emit(can_id, can_data)

        self.data_logger.get_raw_can(can_id, can_data)

    def on_app_exit(self):
        try:
            print("Saving data ...")
            self.data_logger.save_raw_can()
            print("Data successfully saved")
        except OSError:
            raise OSError("Could not save data")
        finally:
            sys.exit()


if __name__ == "__main__":
    app = App()
