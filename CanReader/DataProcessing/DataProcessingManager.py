from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from CanReader.DataProcessing.DataProcessing import DataProcessing
from CanReader.DataProcessing.RawData import RawData


class DataSignal(QObject):
    data_processed = pyqtSignal(list, str, str)


class DataProcessingManager(QRunnable):

    def __init__(self, received_data, data_config_list):
        QRunnable.__init__(self)

        self.received_data = received_data
        self.data_config_list = data_config_list

        self.signal = DataSignal()

    def run(self):
        raw_data = RawData(self.received_data)
        can_id, can_data = raw_data.split_data()

        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        data_to_display = data_decoder.data_decode()

        self.signal.data_processed.emit(data_to_display, can_id, can_data)
