import socket
from network.consts import *
from threading import Thread


class Client:
    def __init__(self, ip, port, ui):
        self.addr = (ip, port)
        self.ui = ui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        self.id = int(self.sock.recv(BUFFSIZE).decode(FORMAT))
        Thread(target=self.listen).start()
        self.players_count = 0

    def listen(self):
        while True:
            self.sock.send("message".encode(FORMAT))
            message = self.sock.recv(BUFFSIZE).decode(FORMAT)
            message = message.split(',')
            self.players_count = int(message[0])

            print(f"Message from server: {message}")
            self.ui.update_player_count(self.players_count, "client")
