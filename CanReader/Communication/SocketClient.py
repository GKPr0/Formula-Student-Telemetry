import logging
import socket

from CanReader.Communication.ComBase import ComBase


class SocketClient(ComBase):
    """
        :Inherit: :class:`ComBase`

        :Description:
            Handle direct communication with car via Wi-Fi.

        :param address: address of socket server
        :type address: str, optional
        :param port: port for socket server
        :type port: int, optional

        :raises OSError:
             IP address is invalid.
        :raises TypeError:
             Port is not a int.
        :raises ValueError:
             Port is not i range 1 - 65536.
    """

    def __init__(self, address='192.168.1.100', port=80):
        ComBase.__init__(self)

        self.check_address(address)
        self.check_port(port)

        self.__address = address
        self.__port = port

    def __repr__(self):
        if self.status == "Offline":
            return "You are disconnected"
        else:
            return "Socket is connected to IP: {} on port {}".format(self.__address, self.__port)

    def close(self):
        """
            :Description:
                Close communication and self destroy.
        """
        self.__sock.close()
        ComBase.close(self)

    def connect_to_device(self):
        """
            :Description:
                Establish serial communication with server via Wi-Fi.\n
                Send information about connection status.

            :raises WindowsError:
                A connection attempt failed because the connected party did not properly respond after
                a period of time, or established connection failed because
                connected host has failed to respond
        """
        try:
            if self.first_connection:
                self.status = "Connecting"
            else:
                self.status = "Reconnecting"
            self.status_changed.emit(self.status)

            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((self.__address, self.__port))
            self.__sock.settimeout(self.TIMEOUT)
            self.first_connection = False
            self.status = "Online"
        except WindowsError:
            logging.warning("A connection attempt failed because the connected party did not properly respond after "
                            "a period of time, or established connection failed because "
                            "connected host has failed to respond", exc_info=True)
            self.running = False
            self.status = "Failed"
        finally:
            self.status_changed.emit(self.status)

    def get_data(self):
        """
            :Description:
                Receive data from device and send signal containing data as a byte array.\n
                Whenever one of the following errors raise, method will try to resolve problem by reconnecting.

            :raises WindowsError:
                Unable to reach network.\n

            :raises AttributeError:
                SocketClient was not set properly.
        """

        while True:
            try:
                if not self.running:
                    break

                data = self.__sock.recv(self.MSG_SIZE)

                if len(data) == 0:
                    break

                self.data_received.emit(bytearray(data))
            except WindowsError:
                # TODO Printovat do GUI do statusbaru
                logging.info("Unable to reach network!")
                self.connect_to_device()
            except AttributeError:
                logging.warning("SocketClient was not set properly", exc_info=True)
                self.connect_to_device()

        self.__sock.close()

    @staticmethod
    def check_address(address):
        """
            :Description:
                Check if IP address is in a valid format.

            :param address: IP address.
            :type address: str

            :raises OSError:
                IP address is not in a valid format.
        """
        try:
            socket.inet_aton(address)
        except OSError:
            error_msg = "IP address is not valid."
            logging.exception(error_msg)
            raise OSError(error_msg)

    @staticmethod
    def check_port(port):
        """
            :Description:
                Check if port is int in range 1 - 65535.

            :param port: Communication port.
            :type port: int

            :raises ValueError:
                Port is not in range of 1 - 65535.

            :raises TypeError:
                Port is not an int.
        """
        try:
            if type(port) != int:
                raise TypeError
            if port <= 0 or port >= 65536:
                raise ValueError
        except ValueError:
            error_msg = "Port number must be in range 1 - 65535."
            logging.exception(error_msg)
            raise ValueError(error_msg)
        except TypeError:
            error_msg = "Port must be integer."
            logging.exception(error_msg)
            raise TypeError(error_msg)

if __name__ == "__main__":
    from datetime import datetime

    def process_data(data):
        id = int.from_bytes(data[:4], "big")
        msg = data[4:]

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time = ", current_time, " ")
        print("ID: {}".format(id))
        for i, m in enumerate(msg):
            print("{}\t{}".format(i, m))

    addr = '192.168.4.1'
    port = 23
    com = SocketClient(addr, port)
    com.data_received.connect(process_data)
    com.connect_to_device()
    print(com)

    while True:
        pass


