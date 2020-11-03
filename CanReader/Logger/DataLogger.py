from PyQt5.QtWidgets import QFileDialog
from datetime import datetime


class DataLogger:
    """
        This class will take care of data logging in specific format

        In future will be extended by *.csv format
    """

    def __init__(self):
        self.raw_data = []
        self.save_path = ""
        self.automatic_path = "./AutomaticDataLog.txt"

    def get_raw_can(self, can_id, can_data):
        """
        Collects incoming data in format:
        "2020/8/5 16:16:27.883		ID:603	Data:1111111100000100000000000000000000000001101100000000010000000010"
        Every 1000 entry save to the file.

        :param can_id: ID of incoming CAN data
        :type can_id: int
        :param can_data: Actual CAN data
        :type can_data: str
        """
        datetime_obj = datetime.now()
        date = str(datetime_obj.year) + "/" + str(datetime_obj.month) + "/" + str(datetime_obj.day)
        time = str(datetime_obj.hour) + ":" + str(datetime_obj.hour)
        time += ":" + str(datetime_obj.second) + "." + str(datetime_obj.microsecond)[:3]
        time_stamp = date + " " + time
        data = "{}\t\tID:{}\tData:{}\n".format(str(time_stamp), can_id, can_data)
        self.raw_data.append(data)

        if len(self.raw_data) > 1000:
            self.save_raw_can()
            self.raw_data.clear()

    def save_raw_can(self):
        """
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
        Open file browser and lets user select save path.
        """
        file_filter = "Text files (*.txt);; All files (*.*)"
        self.save_path = (QFileDialog.getSaveFileName(None, "Save file", "C:\\", file_filter))[0]
