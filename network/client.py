import socket

PORT = 8000
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
BUFFSIZE = 2048

client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)
while True:
    client.send("message".encode(FORMAT))
    message = client.recv(BUFFSIZE).decode(FORMAT)
    print(f"Message from server: {message}")
