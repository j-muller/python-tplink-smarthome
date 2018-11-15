import socket
import json
import struct

from .protocol import encrypt, decrypt


class TPLinkSmartDevice:
    """An object to represent any TP-Link smart device.

    You may not have to instantiate that object directly.
    """

    DEFAULT_PORT = 9999

    def __init__(self, host, port=DEFAULT_PORT, connect=True):
        """Initialize a new smart device object.

        :param host: `string` host to connect to.
        :param port: `int` port to connect to (default: 9999).
        :param connect: `bool` whether you want to connect to the plug on
                        instantiation of the class.
        """
        self.__host = host
        self.__port = port

        self.__socket = None

        if connect:
            self.connect()

    @property
    def host(self):
        """Return the smart device host.
        """
        return self.__host

    @property
    def port(self):
        """Return the smart device port.
        """
        return self.__port

    @property
    def socket(self):
        """Return the socket used to connect to the device.

        Use this property with caution.
        """
        return self.__socket

    def connect(self):
        """Establish a connection to the smart device.
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__host, self.__port))

    def close(self):
        """Close the connection to the smart device.
        """
        # The connection is closed already
        if self.__socket is None:
            return

        self.__socket.close()
        self.__socket = None

    def send(self, command):
        """Send a command to the smart device.

        :param command: `dict` or `string` containing the command to send.
        """
        if isinstance(command, dict):
            command = json.dumps(command)

        if self.__socket is None:
            self.connect()

        self.__socket.send(encrypt(command))

    def recv(self):
        """Wait for data coming from the smart device.
        """
        buffer = bytes()

        # The length of each message is stored in the first 4 bytes.
        while True:
            chunk = self.__socket.recv(4096)
            length, *_ = struct.unpack('>I', chunk[0:4])
            buffer += chunk

            if len(buffer) >= length + 4 or not chunk:
                break

        return json.loads(decrypt(buffer[4:]))
