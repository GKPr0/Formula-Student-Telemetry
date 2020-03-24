from PyQt5.QtWidgets import QFileDialog
import pathlib
from datetime import datetime


class DataLogger:

    def __init__(self):
        self.raw_data = []
        self.file_path = pathlib.Path().absolute()

    def __del__(self):
        pass # @TODO udělat automatické uložení v případě vypnutí

    def get_raw_can(self, raw_can):
        datetime_obj = datetime.now()
        date = str(datetime_obj.year) + "/" + str(datetime_obj.month) + "/" + str(datetime_obj.day)
        time = str(datetime_obj.hour) + ":" + str(datetime_obj.hour) + ":" + str(datetime_obj.second) + "." + str(datetime_obj.microsecond)[:3]
        time_stamp = date + " " + time
        data = str(time_stamp) + "\t" + raw_can + "\n"
        self.raw_data.append(data)

    def save_raw_can(self):
        self.open_file_dialog()
        if self.file_path[0] != "":
            with open(self.file_path[0], "w") as file:
                file.writelines(self.raw_data)
            file.close()

    def open_file_dialog(self):
        file_filter = "Text files (*.txt);; All files (*.*)"
        self.file_path = QFileDialog.getSaveFileName(None, "Save file", "C:\\", file_filter)
