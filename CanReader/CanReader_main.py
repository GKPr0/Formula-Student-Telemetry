import logging
import sys
import threading
from queue import Queue

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThreadPool

from CanReader.Communication.SerialCom import SerialCom
from CanReader.Communication.SocketClient import SocketClient
from CanReader.Config.CanBus.CanConfigHandler import CanConfigHandler
from CanReader.Config.Communication.ComConfigHandler import ComConfigHandler
from CanReader.DataProcessing.DataProcessingManager import DataProcessingManager
from CanReader.GUI.MainWindow import MainWindow
from CanReader.Logger import Logger
from CanReader.Logger.DataLogger import DataLogger


class App:
    """
        :Description:
            This is a main class of whole application.\n
            This class handle communication, data processing and gui as separate threads.\n
            Purpose of this class is to convey data from one task to another one.\n
            Another task of this class is to log received data.
    """

    def __init__(self):
        self.data_logger = DataLogger()
        self.update_config()

        self.processed_data_queue = Queue(maxsize=10)

        self.processing_pool = QThreadPool()
        self.processing_pool.setMaxThreadCount(4)

        # Prepare and run GUI in thread
        self.gui_ready = False
        self.gui = threading.Thread(target=self.run_gui, name='gui')
        self.gui.start()

        self.communication = None

    def start_communication(self, com_type: str):
        """
            :Description:
                Creates and run communication thread depending on communication type.\n
                Connect received data signal with data processing thread function.

            :param com_type: Type of communication Wifi or Serial COM
            :type com_type: str
        """
        if not isinstance(self.communication, (SerialCom, SocketClient)):
            com_config = ComConfigHandler()

            if com_type.lower() == "wifi":
                ip, port = com_config.load_wifi_info()
                self.communication = SocketClient(ip, port)
            elif com_type.lower() == "serial":
                port, baud_rate = com_config.load_serial_info()
                self.communication = SerialCom(port, baud_rate)
            else:
                return

            self.communication.status_changed.connect(self.main_window.update_connection_status_signal.emit)

            self.communication.data_received.connect(self.run_data_processing)

            self.communication.finished.connect(self.communication.deleteLater)
            self.communication.finished.connect(self.delete_communication)

            self.communication.start()

    def stop_communication(self):
        """
            :Description:
                Slot for disconnect signal from UI.\n
                Send signal to communication thread to stop communication and self destroy.
        """
        if isinstance(self.communication, (SerialCom, SocketClient)):
            self.communication.stop_signal.emit()

    def delete_communication(self):
        """
            :Description:
                Used to remove reference to communication address after it was closed.\n
                Garbage collector will do rest when there is no reference pointing to this memory space.
        """
        self.communication = None

    def run_data_processing(self, data_from_formula):
        """
            :Description:
                Run Data Manager as QRunnable in threadpool.\n
                Data Manager sends signal containing DataPoint to data processing queue.\n
                Threadpool is set to have max 4 threads.

            :param data_from_formula: Received data send from communication task.
            :type data_from_formula: bytearray

            .. note::
                Number of threads in threadpool should variable depending on users cpu.
                Max 60% of available threads or so.
        """
        if len(data_from_formula) == 12:
            logging.debug(data_from_formula)
            process_manager = DataProcessingManager(data_from_formula, self.data_config_list)
            process_manager.signal.data_processed.connect(self.receive_processed_data)

            self.processing_pool.start(process_manager)

    def run_gui(self):
        """
            :Description:
                Runs GUI in separate thread, that take cares of data visualization and interaction with user.\n
                Connects all GUI signals with backend slots and vice versa.\n
                Setup GUI update rate.
        """
        gui = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow()

        self.main_window.update_config_signal.connect(self.update_config)
        self.main_window.action_save.triggered.connect(self.data_logger.set_save_path)
        self.main_window.connection_request_signal.connect(self.start_communication)
        self.main_window.disconnect_request_signal.connect(self.stop_communication)
        gui.aboutToQuit.connect(self.on_app_exit)

        self.gui_ready = True

        timer = QtCore.QTimer()

        timer.start(1)
        timer.timeout.connect(self.update_gui)

        sys.exit(gui.exec_())

    def update_config(self):
        """
            :Description:
                Loads Can data config.\n
                Method is called either at booting app or whenever data config is changed.
        """
        config = CanConfigHandler()
        self.data_config_list = config.load_from_config_file()

    def receive_processed_data(self, data_point, can_id, can_data):
        """
            :Description:
                Put data point to the data queue.\n
                If queue is full head is removed.\n
                Send corresponding can id and raw data to data logger and to the main window as status.

            :param data_point: Data point contains real value to be shown and necessary routing config.
            :type: DataPoint

            :param can_id: Can id respectively to data point.
            :param can_id: str

            :param can_data: Can binary data respectively to data point.
            :param can_data: bin
        """
        if self.processed_data_queue.full():
            self.processed_data_queue.get()

        self.processed_data_queue.put(data_point)

        self.main_window.update_can_msg_signal.emit(can_id, can_data)

        self.data_logger.push_raw_can(can_id, can_data)

    def update_gui(self):
        """
            :Description:
                Sends update signal to main window, which runs data queue processing.
        """
        self.main_window.update_data_signal.emit(self.processed_data_queue)

    def on_app_exit(self):
        """
            :Description:
                Invoke just before app will be closed.\n
                Saves collected data regardless of its size.

            :raises OSError:
                Could not save data.
        """
        try:
            logging.debug("Saving data ...")
            self.data_logger.save_raw_can()
            logging.info("App successfully saved")
        except OSError:
            logging.exception("Could not save data")
        finally:
            sys.exit()


if __name__ == "__main__":
    Logger.setup_logger()
    try:
        app = App()
    except Exception:
        logging.exception("Exception in Main():")
        exit(1)
