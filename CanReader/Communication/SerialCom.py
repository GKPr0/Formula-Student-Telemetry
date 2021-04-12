import itertools
import logging
import time
import winreg

from serial import Serial, SerialException

from CanReader.Communication.ComBase import ComBase


class SerialCom(ComBase):
    """
        :Inherit: :class:`ComBase`

        :Description:
            Handle communication with device via serial port (COM).

        :param port: COM port on which to communicate.
        :type port: str

        :param bauds: Baud speed of serial communication
        :type bauds: int, optional

        :raises OSError:
            COM port does not exist.

        :raises TypeError:
            -- COM port is not a str.\n
            -- Baud rate is not a int.

        :raises ValueError:
            Baud rate is not in range 300 - 921600.
    """

    def __init__(self, port, bauds=921600):
        ComBase.__init__(self)

        self.check_com_port(port)
        self.check_baud_rate(bauds)

        self.__port = port.upper()
        self.__baud_rate = bauds

        self.__serial = None

    def __repr__(self):
        if self.status == "Offline":
            return "Device is disconnected"
        else:
            return "Device is connected on COM port: {} with baud rate {}".format(self.__port, self.__baud_rate)

    def close(self):
        """
            :Description:
                Close communication and self destroy.
        """
        if self.__serial is not None:
            self.__serial.close()
        ComBase.close(self)

    def connect_to_device(self):
        """
            :Description:
                Establish serial communication with via USB COM.\n
                Send information about connection status.

            :raises SerialException:
                Port cannot be opened. Usually because port is already opened.
        """
        try:
            if self.first_connection:
                self.status = "Connecting"
            else:
                self.status = "Reconnecting"
            self.status_changed.emit(self.status)

            self.__serial = Serial(port=self.__port, baudrate=self.__baud_rate)
            self.__serial.timeout = self.TIMEOUT
            self.first_connection = False
            self.status = "Online"
        except SerialException:
            logging.warning("Could not open port {}. Port is probably already open!".format(self.__port),
                            exc_info=True)
            self.running = False
            self.status = "Failed"
        finally:
            self.status_changed.emit(self.status)

    def get_data(self):
        """
            :Description:
                Receive data from device and send signal containing data as a byte array.

            :raises:
                If any error occurs try to solve problem by reconnecting to device.
        """

        try:
            if not self.running:
                return

            data = self.__serial.read(self.MSG_SIZE)

            self.data_received.emit(bytearray(data))
        except:
            logging.warning("Error occurred when receiving data", exc_info=True)
            time.sleep(self.TIMEOUT)
            self.connect_to_device()

    @staticmethod
    def available_com_ports() -> list:
        import sys
        """
            :Description:
                Lists serial port names
        
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :raises WindowsError:
                When cannot access COM registers
            :returns:
                A list of the serial ports available on the system
        """
        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        ports = []
        try:
            if not sys.platform.startswith('win'):
                raise EnvironmentError

            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

            for i in itertools.count():
                try:
                    ports.append(winreg.EnumValue(key, i)[1])
                except EnvironmentError:
                    break
        except WindowsError:
            error_msg = "Could not access register on path {}".format(path)
            logging.exception(error_msg)
            raise WindowsError(error_msg)
        except EnvironmentError:
            error_msg = 'Unsupported platform'
            logging.exception(error_msg)
            raise EnvironmentError(error_msg)
        finally:
            return ports

    @staticmethod
    def check_baud_rate(bauds):
        """
            :Description:
                Check if baud is an int in range of 300 - 921600.

            :param bauds: Baud rate.
            :type bauds: int

            :raises ValueError:
                Baud rate is not in range 300 - 921600.

            :raises TypeError:
                Baud rate is not an integer.
        """
        try:
            if type(bauds) != int:
                raise TypeError
            if bauds < 300 or bauds > 921600:
                raise ValueError
        except ValueError:
            error_msg = "Baud rate must be in range 300 - 921600!"
            logging.exception(error_msg)
            raise ValueError(error_msg)
        except TypeError:
            error_msg = "Baud rate must be an integer!"
            logging.exception(error_msg)
            raise TypeError(error_msg)

    @staticmethod
    def check_com_port(port):
        """
            :Description:
                Check if port is a str and can be found on the system.

            :param port: Com port name.
            :type port: str

            :raises TypeError:
                Port is not a str.

            :raises OSError:
                Port cannot be find on the system.
        """
        try:
            if type(port) != str:
                raise TypeError
            if port.upper() not in SerialCom.available_com_ports():
                raise OSError
        except OSError:
            error_msg = "Cannot find port {}!".format(port)
            logging.exception(error_msg)
            raise OSError(error_msg)
        except TypeError:
            error_msg = "COM port must be a string!"
            logging.exception(error_msg)
            raise TypeError(error_msg)


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
