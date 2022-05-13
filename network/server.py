import time
import socket
import random
import numpy as np
from threading import Thread
from network.consts import *
from algorithms.maze_generator import generate_maze
from game import consts as gm_const
from network.string_processing import *


def create_exits(maze):
    probably_exit = []
    for i in range(maze.shape[1]):
        if maze[i][-2] == gm_const.FLOOR:
            probably_exit.append([i, -1])
    exit = random.choice(probably_exit)
    maze[exit[0], exit[1]] = gm_const.FINISH
    return maze


def maze_to_str(maze, shape):
    maze = maze.reshape(shape[0] * shape[1])
    maze = [str(cell) for cell in maze]
    maze_str = ''.join([cell + ', ' for i, cell in enumerate(maze) if i < len(maze) - 1]) + maze[-1]
    return maze_str


def set_rats_in_maze(maze, rat_count):
    rat_poses = []
    for i in range(maze.shape[1]):
        if maze[i][1] == gm_const.FLOOR:
            rat_poses.append([1, i])
    random.shuffle(rat_poses)

    return [rat_poses[i] for i in range(rat_count)]


class Bot:
    def __init__(self, server, pos, id):
        self.id = id
        self.server = server
        self.pos = pos
        self.maze_vision = self.create_vision(self.server.maze)
        self.prev_poses = []

    def create_vision(self, maze):
        maze_shape = maze.shape
        maze_vision = np.full(maze_shape, 2)
        return maze_vision

    def _check_neighbor_cell(self, dir):
        x, y = self.pos
        if dir == 'up':
            y -= 1
        elif dir == 'down':
            y += 1
        elif dir == 'left':
            x -= 1
        elif dir == 'right':
            x += 1
        return True if self.maze_vision[y, x] == gm_const.BLIND or \
                       self.maze_vision[y, x] == gm_const.RAT or \
                       self.maze_vision[y, x] == gm_const.FLOOR else False

    def _get_directions(self):
        directions = []
        x, y = self.pos
        if self._check_neighbor_cell('up'):
            directions.append([x, y - 1])
        if self._check_neighbor_cell('down'):
            directions.append([x, y + 1])
        if self._check_neighbor_cell('left'):
            directions.append([x - 1, y])
        if self._check_neighbor_cell('right'):
            directions.append([x + 1, y])
        return directions

    def _open_maze_cell(self, pos):
        cell = self.server.maze[pos[1], pos[0]]
        self.maze_vision[pos[1], pos[0]] = cell
        if cell == gm_const.FINISH:
            self.server.escaped = 1

    def step(self):
        directions = self._get_directions()
        if len(directions) > 0:
            new_pos = random.choice(directions)
            self._open_maze_cell(new_pos)
            self.prev_poses.append(self.pos)
            if self.maze_vision[new_pos[1], new_pos[0]] == gm_const.FLOOR or \
                    self.maze_vision[new_pos[1], new_pos[0]] == gm_const.RAT:
                self.pos = new_pos
                self.server.rats[self.id] = [new_pos[0], new_pos[1]]
                self.maze_vision[new_pos[1], new_pos[0]] = gm_const.WAS_HERE
        elif len(self.prev_poses) > 0:
            self.pos = self.prev_poses.pop()


class Server:
    def __init__(self, ip, port, ui, bots):
        self.addr = (ip, port)
        self.ui = ui
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.bots_count = bots
        self.sock.bind(self.addr)
        self.clients = []
        self.run_game = True
        self.status = 'wait'
        self.escaped = 0
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
        self.status = 'init'

    def send_game_status(self):
        while self.run_game:
            time.sleep(0.7)
            for i, client in enumerate(self.clients):
                print(f"wait message from {i}")
                message = client.recv(BUFFSIZE).decode(FORMAT)
                escaped, coords = message.split(';')
                self.escaped = int(escaped)
                coords = coords.split(',')
                if self.status == GAME:
                    self.rats[i][0], self.rats[i][1] = int(coords[0]), int(coords[1])
                    self.maze[self.rats[i][1], self.rats[i][0]] = gm_const.RAT
                print(f"message from {i}: {message}")

            message = ''
            if self.status == WAIT:
                message = f'{WAIT}; {len(self.clients)}'

            elif self.status == INIT:
                """
                there will be a code for generate maze and player's coords
                """

                shape = (11, 11)
                self.maze = generate_maze(shape, threshold=0.85)
                self.maze = create_exits(self.maze)
                self.rats = set_rats_in_maze(self.maze, len(self.clients) + self.bots_count)
                self.bots = [Bot(self, self.rats[len(self.clients) + i], len(self.clients) + i) for i in range(self.bots_count)]
                maze_str = maze_to_str(self.maze, shape)
                rats_str = rats_to_str(self.rats)
                message = f'{INIT};{maze_str};sh_0={shape[0]};sh_1={shape[1]};{rats_str}'
                self.status = GAME

            elif self.status == GAME:
                for bot in self.bots:
                    bot.step()
                rats_str = rats_to_str(self.rats)
                message = f"{GAME};{self.escaped};{rats_str}"

            for client in self.clients:
                client.send(message.encode(FORMAT))
