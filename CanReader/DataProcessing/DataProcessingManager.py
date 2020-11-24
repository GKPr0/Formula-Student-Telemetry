from PyQt5.QtCore import QRunnable, pyqtSignal
from DataProcessing.RawData import RawData
from DataProcessing.DataProcessing import DataProcessing
from DataProcessing.DataPoint import DataPoint
from Logger.DataLogger import DataLogger


class DataProcessingManager(QRunnable):

    data_processed = pyqtSignal(DataPoint, str, str)

    def __init__(self, received_data, data_config_list):
        QRunnable.__init__(self)

        self.received_data = received_data
        self.data_config_list = data_config_list

    def run(self):
        raw_data = RawData(self.received_data)
        can_id, can_data = raw_data.split_data()
        print("ID: " + can_id)
        print("data: " + can_data)

        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        data_to_display = data_decoder.data_decode()

        self.data_processed.emit(data_to_display, can_id, can_data)
