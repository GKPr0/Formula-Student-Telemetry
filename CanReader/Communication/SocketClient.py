import socket
import logging
from Communication.ComBase import ComBase


class SocketClient(ComBase):
    """
        This class will ensure communication with remote device.

        :param address: address of socket server
        :type address: str
        :param port: port for socket server
        :type port: int

        :raises OSError:
            - IP address is invalid.
        :raises TypeError:
            - Port is not a int.
        :raises ValueError:
            - Port is not i range 1 - 65536.


        - Example of valid constructor::

            socket_client = SocketClient("192.168.1.100", 32001)

        - Example of invalid constructor::

            socket_client = SocketClient("A92.168.1.100", 320001)

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
        self.__sock.close()
        ComBase.close(self)

    def connect_to_device(self):
        """
        Establish communication with server(ESP32).
        """
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((self.__address, self.__port))
            self.__sock.settimeout(3)
            self.status = "Online"
        except WindowsError:
            logging.warning("A connection attempt failed because the connected party did not properly respond after "
                            "a period of time, or established connection failed because "
                            "connected host has failed to respond")
            self.status = "Offline"
        finally:
            self.status_changed.emit(self.status)

    def get_data(self):
        """
            Receive data from server and send signal containing data a byte array.
        """

        while True:
            try:
                if not self.run:
                    break

                data = self.__sock.recv(self.MSG_SIZE)

                if len(data) == 0:
                    break

                self.data_received.emit(bytearray(data))
            except WindowsError:
                # TODO Printovat do GUI do statusbaru
                logging.warning("Unable to reach network!")
                self.status = "Offline"
                self.status_changed.emit(self.status)
                self.connect_to_device()
            except AttributeError:
                logging.exception("SocketClient was not set properly")
                self.connect_to_device()

        self.__sock.close()

    @staticmethod
    def check_address(address):
        """
            Check validity of IP address.
        """
        try:
            socket.inet_aton(address)
        except OSError:
            logging.exception("IP address is not valid.")

    @staticmethod
    def check_port(port: int):
        """
            Check validity of port type and range.
        """
        try:
            if port <= 0 or port >= 65536:
                raise ValueError
        except ValueError:
            logging.exception("Port number must be in range 1 - 65535.")
        except TypeError:
            logging.exception("Port must be integer.")

if __name__ == "__main__":
    """
        Useful for communication test
    """
    from datetime import datetime

    def process_data(data):
        id = int.from_bytes(data[:4], "big")
        msg = data[4:]

        print("ID: {}".format(id))
        for i, m in enumerate(msg):
            print("{}\t{}".format(i, m))

    addr = '192.168.1.100'
    port = 80
    com = SocketClient(addr, port)
    com.data_received.connect(process_data)
    com.connect_to_server()
    print(com)

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time = ", current_time , " ")

