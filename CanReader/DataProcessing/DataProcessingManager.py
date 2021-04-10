from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from CanReader.DataProcessing.DataProcessing import DataProcessing
from CanReader.DataProcessing.RawData import RawData


class DataSignal(QObject):
    """
        :Inherit: :class:`QObject`

        :Description:
            Helper class for :class:`DataProcessingManager` allowing usage of Qt Signal.
    """
    data_processed = pyqtSignal(list, str, str)


class DataProcessingManager(QRunnable):
    """
        :Inherit: :class:`QRunnable`

        :Description:
            This class inherit from QRunnable -> can run as separate task.\n
            Takes care of data processing flow.\n
            Data to superior task are being passed with Qt Signal.

        :param received_data: Received data in raw format.
        :type received_data: bytearray

        :param data_config_list: List of data configurations
        :type data_config_list: list[CanDataConfig]
    """

    def __init__(self, received_data, data_config_list):
        QRunnable.__init__(self)

        self.received_data = received_data
        self.data_config_list = data_config_list

        self.signal = DataSignal()

    def run(self):
        """
            :Description:
                Runs data processing sequence:
                    1. Split received data to ID and Data.
                    2. Decode and processed data based on configuration.
                    3. Send data to superior task with QtSignal
        """
        raw_data = RawData(self.received_data)
        can_id, can_data = raw_data.split_data()

        data_decoder = DataProcessing(can_id, can_data, self.data_config_list)
        data_to_display = data_decoder.data_decode()

        self.signal.data_processed.emit(data_to_display, can_id, can_data)
