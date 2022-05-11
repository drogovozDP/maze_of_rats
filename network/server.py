import time
import socket
from threading import Thread


FORMAT = 'utf-8'
BUFFSIZE = 2048
run_game = True


class Server:
    def __init__(self, ip, port):
        self.addr = (ip, port)
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.clients = []

    def init_game(self):
        Thread(target=self.send_game_status, args=()).start()

    def listen(self):
        self.sock.listen()
        self.init_game()
        print("Wait for connection")
        while run_game:
            conn, addr = self.sock.accept()
            conn.send("hi".encode(FORMAT))
            self.clients.append(conn)
            print(f"Client {addr} just connected")

    def send_game_status(self):
        while True:
            time.sleep(1)
            for i, client in enumerate(self.clients):
                message = client.recv(BUFFSIZE).decode(FORMAT)
                print(f"message from {i}: {message}")
                client.send(f"message {i}".encode(FORMAT))


if __name__ == '__main__':
    server = Server('127.0.0.1', 8000)
    server.listen()
    print('kek')