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

    def push_raw_can(self, can_id, can_data):
        """
        :Description:
            Push incoming data to the storage if there is difference:\n
            Every 1000 entry save to the file.\n

        :param can_id: ID of incoming CAN data
        :type can_id: str
        :param can_data: Actual CAN data
        :type can_data: str
        """
        if self.is_can_data_modified(can_id, can_data):
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
        update = True
        if can_id in self.can_dict:
            if can_data == self.can_dict[can_id]:
                update = False

        if update:
            self.can_dict[can_id] = can_data
            return True
        else:
            return False

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
