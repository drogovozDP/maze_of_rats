import socket


class Network:
    def __init__(self, addr, port, buffer_size=1024):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = (addr, port)
        self.buffer_size = buffer_size
        self.position = self.connect()

    def get_position(self):
        return self.position

    def connect(self):
        self.client.connect(self.server)
        return self.client.recv(self.buffer_size).decode()

    def send(self, data):
        self.client.send(str.encode(data))
        return self.client.recv(self.buffer_size).decode()
