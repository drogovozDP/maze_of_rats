import socket
from network.consts import *
from threading import Thread
from game.game_client import GameClient
from network.string_processing import *


class Client:
    def __init__(self, ip, port, ui):
        self.addr = (ip, port)
        self.ui = ui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        self.id = int(self.sock.recv(BUFFSIZE).decode(FORMAT))
        self.game_client = None
        Thread(target=self.listen).start()
        self.players_count = 0

    def listen(self):
        while True:
            message_to_server = '0;-1,-1'
            self.sock.send(message_to_server.encode(FORMAT))
            message = self.sock.recv(BUFFSIZE).decode(FORMAT)

            print(message)
            message = message.split(';')

            if message[0] == WAIT:
                print(f"Message from server: {message}")
                self.ui.update_player_count(self.players_count, "client")
                self.players_count = int(message[1])
            elif message[0] == INIT:
                maze_str = message[1]
                shape = (int(message[2][5:]), int(message[3][5:]))
                rats = rats_from_str(message[4])

                # Thread(target=GameClient, args=(self.id, rats, maze_str, shape, self)).start()

                GameClient(
                    this_player=self.id,
                    players=rats,
                    maze_str=maze_str,
                    maze_shape=shape,
                    network=self.sock
                )

                self.ui.window.destroy()
