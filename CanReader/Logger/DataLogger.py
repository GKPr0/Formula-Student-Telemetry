from datetime import datetime

from PyQt5.QtWidgets import QFileDialog


class DataLogger:
    """
        :Description:
            This class takes care of data logging in specific format.\n
            Currently is logging only raw data.\n
            To save some storage only differences are saved. \n
            For specific ID new data will be saved only if there is difference in at least one bit.\n

        .. note::
            Currently only txt format is supported, in future *.csv format will be available as well.
    """

    def __init__(self):
        self.raw_data = []
        self.save_path = ""
        self.automatic_path = "./AutomaticDataLog.txt"
        self.can_dict = {}

    def get_raw_can(self, can_id, can_data):
        """
        :Description:
            Collects incoming data in format:\n
            "2020/8/5 16:16:27.883		ID:603	Data:1111111100000100000000000000000000000001101100000000010000000010"\n
            Every 1000 entry save to the file.\n

        :param can_id: ID of incoming CAN data
        :type can_id: str
        :param can_data: Actual CAN data
        :type can_data: str
        """

        time_stamp = DataLogger.get_timestamp()

        data = "{}\t\tID:{}\tData:{}\n".format(str(time_stamp), can_id, can_data)
        self.raw_data.append(data)

        if len(self.raw_data) > 1000:
            self.save_raw_can()
            self.raw_data.clear()

    def is_can_data_modified(self, can_id, can_data):
        """
        :Description:
            Check if incoming data are different then last record for given can id.

        :param can_id: Id of can msg.
        :type can_id: str

        :param can_data: Can data in binary format
        :type can_data: str

        :return: True if data on specific id do not mach saved data
        :rtype: bool
        """

    def save_raw_can(self):
        """
            :Description:
                Save collected data to automatic path or user defined path in *.txt format.
        """
        if self.save_path == "":
            path = self.automatic_path
        else:
            path = self.save_path

        with open(path, "a") as file:
            file.writelines(self.raw_data)

    def set_save_path(self):
        """
            :Description:
                Open a file browser and let the user choose a save path.
        """
        file_filter = "Text files (*.txt);; All files (*.*)"
        self.save_path = (QFileDialog.getSaveFileName(None, "Save file", "C:\\", file_filter))[0]

    @staticmethod
    def get_timestamp():
        """
            :Description:
                Generate timestamp in format YY/MM/DD HH:MM:SS:uS.
        """
        datetime_obj = datetime.now()
        date = str(datetime_obj.year) + "/" + str(datetime_obj.month) + "/" + str(datetime_obj.day)

        time = str(datetime_obj.hour) + ":" + str(datetime_obj.minute)
        time += ":" + str(datetime_obj.second) + "." + str(datetime_obj.microsecond)[:3]

        return date + " " + time
