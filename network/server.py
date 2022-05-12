import time
import socket
from threading import Thread
from network.consts import *


FORMAT = 'utf-8'
BUFFSIZE = 2048


class Server:
    def __init__(self, ip, port, ui):
        self.addr = (ip, port)
        self.ui = ui
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.clients = []
        self.run_game = True
        self.status = 'wait'
        self.sock.listen()
        Thread(target=self.listen).start()
        Thread(target=self.send_game_status).start()
        print("Wait for connection")

    def listen(self):
        while True:
            conn, addr = self.sock.accept()
            conn.send(f"{len(self.clients)}".encode(FORMAT))
            self.clients.append(conn)
            self.ui.update_player_count(len(self.clients), "server")
            print(f"Client {addr} just connected")

    def start_game(self):
        print("start game")

    def send_game_status(self):
        while self.run_game:
            time.sleep(1)
            for i, client in enumerate(self.clients):
                message = client.recv(BUFFSIZE).decode(FORMAT)
                print(f"message from {i}: {message}")

            message = ''
            if self.status == 'wait':
                message = f'wait; {len(self.clients)}'

            for client in self.clients:
                client.send(message.encode(FORMAT))
