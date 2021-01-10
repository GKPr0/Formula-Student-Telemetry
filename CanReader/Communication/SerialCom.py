# !/usr/bin/python3

from serial import Serial, SerialException
from Communication.ComBase import ComBase
import time
import winreg
import itertools


class SerialCom(ComBase):
    """
    Ensures serial communication with receiver(ESP32).
    Baud rate is specified by connected device.
    Max baud rate is given by UART-USB convertor (CP2102 -> 926100 bauds)

        :param port: COM port on which is connected device
        :type port: str
        :param bauds: Baud speed of serial communication
        :type bauds: int


        :raises OSError:
            - COM port odes not exist.
        :raises TypeError:
            - COM port is not a str.
            - Baud rate is not a int.
        :raises ValueError:
            - Baud rate is not in range 300 - 921600.
    """

    def __init__(self, port, bauds=921600):
        ComBase.__init__(self)

        self.check_com_port(port)
        self.check_baud_rate(bauds)

        self.__port = port
        self.__baud_rate = bauds

    def __repr__(self):
        if self.status == "Offline":
            return "Device is disconnected"
        else:
            return "Device is connected on COM port: {} with baud rate {}".format(self.__port, self.__baud_rate)

    def close(self):
        self.__serial.close()
        ComBase.close(self)

    def connect_to_device(self):
        """
            Establish communication with receiver(ESP32).
        """
        try:
            self.__serial = Serial(port=self.__port, baudrate=self.__baud_rate)
            self.__serial.timeout = 1
            self.status = "Online"
        except SerialException:
            self.status = "Offline"
            raise SerialException("Could not open port {}. Port is probably already open!".format(self.__port))
        finally:
            self.status_changed.emit(self.status)

    def get_data(self):
        """
            Receive data from device and send signal containing data a byte array.
        """

        try:
            if not self.run:
                return

            data = self.__serial.read(self.MSG_SIZE)

            self.data_received.emit(bytearray(data))
        except:
            print("Error occurred when receiving data")
            self.status = "Offline"
            self.status_changed.emit(self.status)
            time.sleep(self.TIMEOUT)
            self.connect_to_device()

    @staticmethod
    def available_com_ports() -> list:
        import sys
        """
            Lists serial port names
        
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :raises WindowsError:
                When cannot access COM registers
            :returns:
                A list of the serial ports available on the system
        """
        if not sys.platform.startswith('win'):
            raise EnvironmentError('Unsupported platform')

        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        ports = []

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

            for i in itertools.count():
                try:
                    ports.append(winreg.EnumValue(key, i)[1])
                except EnvironmentError:
                    break

        except WindowsError:
            raise WindowsError("Could not access register on path {}".format(path))
        finally:
            return ports

    @staticmethod
    def check_baud_rate(bauds: int):
        try:
            if bauds < 300 or bauds > 921600:
                raise ValueError
        except ValueError:
            raise ValueError("Baud rate must be in range 300 - 921600!")
        except TypeError:
            raise TypeError("Baud rate must be an integer!")

    @staticmethod
    def check_com_port(port: str):
        try:
            if port not in SerialCom.available_com_ports():
                raise OSError
        except OSError:
            raise OSError("Cannot find port {}!".format(port))
        except TypeError:
            raise TypeError("COM port must be a string!")


if __name__ == "__main__":
    """
    ser = serial.Serial('COM4', 921600, timeout=None) #921600 buad is max speed of cp2102

    startTime = time.time()
    i = 0
    while i < 125000:
        i += len(ser.read(ser.inWaiting())) # 1.35 sec on 1Mbit
    print(time.time() - startTime)
    """
    def print_data(data: bytearray):
        print(data)

    serCom = SerialCom('COM4', 921600)
    serCom.data_received.connect(print_data)
    serCom.connect_to_device()
    while 1:
        serCom.get_data()






