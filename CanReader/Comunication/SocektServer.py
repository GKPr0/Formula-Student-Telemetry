"""
Class socket server will ensure communication with remote device. Data can be received with method called "get_data()".
"""

import socket

class SocketServer:

    def __init__(self, address, port):
        # Check if address and port are valid
        self.check_address(address)
        self.check_port_value(port)
        self.check_port_type(port)

        self.__address = address
        self.__port = port
        self.__set()

    def __repr__(self):
        return "Socket is connected to IP: {} on port {}".format(self.__address, self.__port)

    def __set(self):
        # Prepare socket to begin communication
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((self.__address, self.__port))
        self.__sock.listen(0)

    def get_data(self):
        # Receive data from client and return them as a string
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
        # Will check validity of IP address
        try:
            socket.inet_aton(address)
        except OSError:
            raise OSError("IP address in not valid.")

    @staticmethod
    def check_port_value(port):
        # Will check validity of port range, must be in range of 1 to 65535
        try:
            if port <= 0 or port >= 65535:
                raise ValueError
        except ValueError:
            raise ValueError("Port number must be in range 1 - 65535.")

    @staticmethod
    def check_port_type(port):
        # Will check validity of port type, must be int
        try:
            if type(port) != int:
                raise TypeError
        except TypeError:
            raise TypeError("Port must be integer.")



