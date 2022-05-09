import socket
from _thread import*


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server, port))
        self.socket.listen(2)
        self.buffer_size = 1024
        print("Waiting for connection, Server Started")
        self.currentPlayer = 0

    def read_pos(self, pos):
        pos = pos.split(",")
        return int(pos[0]), int(pos[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def threaded_client(self, conn, player):
        conn.send(str.encode(self.make_pos(pos[player])))
        while True:
            data = conn.recv(self.buffer_size).decode()
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                data = self.read_pos(data)
                pos[player] = data

                if player == 1:
                    reply = self.make_pos(pos[0])
                else:
                    reply = self.make_pos(pos[1])
                conn.send(str.encode(reply))
        print(f"Lost connection with player {player}")
        self.currentPlayer -= 1
        conn.close()

    def listen(self):
        while True:
            conn, addr = self.socket.accept()
            print("Connected to:", addr)
            # запускает функцию параллельно относительно остальных процессов
            start_new_thread(self.threaded_client, (conn, self.currentPlayer))
            print(self.currentPlayer)
            self.currentPlayer += 1


server = "127.0.0.1"
port = 8000
pos = [(100, 10), (50, 50)]

server = Server(server, port)
server.listen()
print("TYTA")
