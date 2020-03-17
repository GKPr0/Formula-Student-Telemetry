import socket


class SocketClient:
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

            socket_server = SocketServer("192.168.1.100", 32001)

        - Example of invalid constructor::

            socket_server = SocketServer("A92.168.1.100", 320001)

    """

    def __init__(self, address, port):

        self.check_address(address)
        self.check_port(port)

        self.__address = address
        self.__port = port
        self.__set()

    def __repr__(self):
        return "Socket is connected to IP: {} on port {}".format(self.__address, self.__port)

    def __set(self):
        """
        Establish communication with server(ESP32).
        """
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__address, self.__port))

    def get_data(self):
        """
        This function will receive data from server and return them as a str.

        :return: received data (:py:class:`str`)
        """

        # TODO Změnit na příjem HEX

        while True:
            data = self.__sock.recv(1024)

            if len(data) == 0:
                break

            return str(data.decode())

        self.__sock.close()

    @staticmethod
    def check_address(address):
        """
            Check validity of IP address.
        """

        try:
            socket.inet_aton(address)
        except OSError:
            raise OSError("IP address in not valid.")

    @staticmethod
    def check_port(port):
        """
            Check validity of port type and range.
        """

        try:
            if port <= 0 or port >= 65536:
                raise ValueError
            if type(port) != int:
                raise TypeError
        except ValueError:
            raise ValueError("Port number must be in range 1 - 65535.")
        except TypeError:
            raise TypeError("Port must be integer.")


if __name__ == "__main__":

    from datetime import datetime

    addr = '192.168.1.100'
    port = 80
    com = SocketClient(addr, port)
    count = 0
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time = ", current_time , " ")
        print(com.get_data() + str(count), "\n")
        count += 1
