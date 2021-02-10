import logging
import time

from PyQt5.QtCore import QThread, pyqtSignal


class ComBase(QThread):
    status_changed = pyqtSignal(str)
    data_received = pyqtSignal(bytearray)
    stop_signal = pyqtSignal()

    MSG_SIZE = 12  # bytes
    TIMEOUT = 1  # sec

    def __init__(self):
        QThread.__init__(self)
        self.status = "Offline"
        self.running = True
        self.first_connection = True

        self.stop_signal.connect(self.stop_com)

    def __del__(self):
        logging.debug("Com deleted")

    def stop_com(self):
        self.running = False
        self.close()

    def close(self):
        self.status = "Offline"
        self.status_changed.emit(self.status)
        self.quit()
        logging.debug("Com closing")

    def connect_to_device(self):
        raise NotImplementedError()

    def get_data(self):
        raise NotImplementedError()

    def run(self):
        """
            This method is called when thread is started with start() method.
            Main communication loop
        """
        while self.status == "Offline":
            self.connect_to_device()

        while self.running:
            self.get_data()
            time.sleep(0.0005)

        self.close()
