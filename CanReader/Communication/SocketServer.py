"""
.. module:: SocketServer
   :synopsis: Contains model of communication

.. moduleauthor:: Ondrej Vacek

"""

import socket

class SocketServer:
    """
        This class will ensure communication with remote device.

        :param address: address of socket server
        :type address: str
        :param port: port for socket server
        :type port: int

        :raises OSError: If invalid IP address is given. Validity is handled by inner socket method
        :raises TypeError: If port is not a int
        :raises ValueError: If port is not i range 1 - 65536


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
        Prepare socket to begin communication.
        """

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((self.__address, self.__port))
        self.__sock.listen(0)

    def get_data(self):
        """
        This function will received data from connected client and return them as a string.

        :return: received data (:py:class:`str`)
        """

        # TODO Změnit na příjem HEX
        client, addr = self.__sock.accept()

        while True:
            data = client.recv(22)

            if len(data) == 0:
                break
            else:
                return str(data.decode())

        client.close()

    @staticmethod
    def check_address(address):
        #Check validity of IP address.

        try:
            socket.inet_aton(address)
        except OSError:
            raise OSError("IP address in not valid.")

    @staticmethod
    def check_port(port):
        #Check validity of port type and range.

        try:
            if port <= 0 or port >= 65536:
                raise ValueError
            if type(port) != int:
                raise TypeError
        except ValueError:
            raise ValueError("Port number must be in range 1 - 65535.")
        except TypeError:
            raise TypeError("Port must be integer.")





