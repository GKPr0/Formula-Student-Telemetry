from PyQt5.QtWidgets import QFileDialog
import pathlib
from datetime import datetime


class DataLogger:

    def __init__(self):
        self.raw_data = []
        self.save_path = ""
        self.automatic_path = "./AutomaticDataLog.txt"

    def __del__(self):
        pass # @TODO udělat automatické uložení v případě vypnutí

    def get_raw_can(self, raw_can):
        datetime_obj = datetime.now()
        date = str(datetime_obj.year) + "/" + str(datetime_obj.month) + "/" + str(datetime_obj.day)
        time = str(datetime_obj.hour) + ":" + str(datetime_obj.hour) + ":" + str(datetime_obj.second) + "." + str(datetime_obj.microsecond)[:3]
        time_stamp = date + " " + time
        data = str(time_stamp) + "\t\t" + raw_can + "\n"
        self.raw_data.append(data)
        if len(self.raw_data) > 1000:
            self.save_raw_can()
            self.raw_data.clear()

    def save_raw_can(self):
        if self.save_path == "":
            path = self.automatic_path
        else:
            path = self.save_path

        with open(path, "a") as file:
            file.writelines(self.raw_data)

    def set_save_path(self):
        file_filter = "Text files (*.txt);; All files (*.*)"
        self.save_path = (QFileDialog.getSaveFileName(None, "Save file", "C:\\", file_filter))[0]
