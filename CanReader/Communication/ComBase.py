from PyQt5.QtCore import QThread, pyqtSignal
import time


class ComBase(QThread):

    status_changed = pyqtSignal(str)
    data_received = pyqtSignal(bytearray)
    stop_signal = pyqtSignal()

    MSG_SIZE = 12  # bytes
    TIMEOUT = 1  # sec

    INSTANCE_COM_LIST = []

    def __init__(self):
        QThread.__init__(self)
        ComBase.INSTANCE_COM_LIST.append(self)
        self.status = "Offline"
        self.run = True

        self.stop_signal.connect(self.stop_com)

    def __del__(self):
        print("Com deleted")

    def stop_com(self):
        self.run = False

    def close(self):
        self.status = "Offline"
        self.status_changed.emit(self.status)
        self.quit()
        print("Com closing")

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

        while self.run:
            self.get_data()
            time.sleep(0.0005)

        self.close()
