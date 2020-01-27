"""
Main handler of project.

"""
from CanReader.Config.Config import Config
from CanReader.Communication.SocketServer import SocketServer
from CanReader.DataProcessing.RawData import RawData
from CanReader.DataProcessing.DataPoint import DataPoint
from CanReader.DataProcessing.DataProcessing import DataProcessing

if __name__ == "__main__":

    config_file_name = "config_file.ini"
    data_esp = "ID100XAB000800B00C00"

    config = Config(config_file_name)
    data_config_list = config.load_from_config_file()

    raw_data = RawData(data_esp)
    can_id, can_data = raw_data.split_data()
    data_decoder = DataProcessing(can_id, can_data, data_config_list)
    data = data_decoder.data_decode()
    print(can_data)
    print(data)