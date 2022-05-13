import pygame as pg
import numpy as np
from game.consts import *
from game.graphic import Graphic
from threading import Thread
from network.consts import BUFFSIZE, FORMAT
from network.string_processing import rats_from_str


class Entity:
    def __init__(self, client, x, y, color):
        self.client = client
        self.x = x
        self.y = y
        self.color = color
        self.size = self.client.graphic.cell_size
        self.padding = self.client.graphic.cell_pad

    def draw(self):
        x = self.padding[0] + self.x * self.size
        y = self.padding[1] + self.y * self.size
        self.client.pg.draw.rect(self.client.screen, self.color,
                                 self.client.pg.Rect(x, y, self.size, self.size))


class Rat(Entity):
    def __init__(self, client, x, y, id, color):
        super().__init__(client, x, y, color)
        self.velocity = 1
        self.maze_vision = self.create_vision()
        self.id = id
        self.dx = 0
        self.dy = 0
        self.escaped = 0
        self.image = self.client.pg.image.load(SPRITE_DIR / 'this_rat.png') \
            if self.id == self.client.this_player else \
            self.client.pg.image.load(SPRITE_DIR / 'enemy_rat.png')
        self.cell_size = self.client.graphic.cell_size
        self.image = self.client.pg.transform.scale(self.image, (self.cell_size, self.cell_size))

    def draw(self):
        if self.id != self.client.this_player and self.client.this_rat.maze_vision[self.y, self.x] == BLIND:
            return
        cell_pad = self.client.graphic.cell_pad
        self.client.screen.blit(self.image, self.image.get_rect(
            center=(self.x * self.cell_size + cell_pad[0] + self.image.get_size()[0] // 2,
                    self.y * self.cell_size + cell_pad[1] + self.image.get_size()[1] // 2)
            )
        )

    def create_vision(self):
        maze_shape = self.client.maze.shape
        maze_vision = np.full(maze_shape, 2)
        return maze_vision

    def update_maze(self, x, y):
        self.client.maze[self.y, self.x] = FLOOR
        self.client.maze[y, x] = RAT
        self.x = x
        self.y = y

    def set_dxdy(self, direction):
        dx, dy = 0, 0
        if direction == 'up':
            dx, dy = 0, -self.velocity
        elif direction == 'down':
            dx, dy = 0, self.velocity
        elif direction == 'left':
            dx, dy = -self.velocity, 0
        elif direction == 'right':
            dx, dy = self.velocity, 0
        self.dx = dx
        self.dy = dy

    def check_collision(self):
        x = self.x + self.dx
        y = self.y + self.dy
        if y == self.client.maze.shape[0] or x == self.client.maze.shape[1]:
            self.dx, self.dy = 0, 0
            return
        self.maze_vision[y, x] = self.client.maze[y, x]
        cell = self.client.maze[y, x]
        if cell == FLOOR or cell == FINISH:
            self.update_maze(x, y)
            if cell == FINISH:
                self.escaped = 1
        self.dx, self.dy = 0, 0

    def move(self):
        self.check_collision()


class GameClient:
    """
    This class takes dict of players {id: coords}, current player's id, string
    of maze and shape for it.
    """

    def __init__(self, this_player, players, maze_str, maze_shape, network):
        # pygame standard init
        self.pg = pg
        self.screen = self.pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = self.pg.time.Clock()
        self.FPS = 60
        self.running = True

        # network
        self.network = network

        # create maze
        self.maze = self.create_maze_from_str(maze_str, maze_shape, players)
        self.graphic = Graphic(self)

        self.this_player = this_player  # current player id
        self.rats = self.create_rats(players)  # create rats
        self.this_rat = self.rats[self.this_player]  # current rat
        self.server_listener = Thread(target=self.listen_server)
        self.server_listener.start()
        self.run()

    def create_rats(self, players):
        rats = []
        for id, coords in enumerate(players):
            rats.append(Rat(self, coords[0], coords[1], id, (255, 0, 0)))
        return rats

    def create_maze_from_str(self, maze_str, maze_shape, players):
        maze = np.array([int(cell) for cell in maze_str.split(', ')]).reshape(maze_shape)
        for rat in players:
            maze[rat[1], rat[0]] = RAT
        return maze

    def this_player_input(self):
        for event in self.pg.event.get():
            if event.type == self.pg.QUIT:
                self.running = False
        keys = self.pg.key.get_pressed()
        if keys[self.pg.K_UP]:
            self.this_rat.set_dxdy('up')
        if keys[self.pg.K_DOWN]:
            self.this_rat.set_dxdy('down')
        if keys[self.pg.K_LEFT]:
            self.this_rat.set_dxdy('left')
        if keys[self.pg.K_RIGHT]:
            self.this_rat.set_dxdy('right')

    def update_screen(self):
        self.clock.tick(self.FPS)
        self.screen.fill(COLOR['bg'])
        self.graphic.draw_environment()
        self.pg.display.update()

    def run(self):
        while self.running:
            self.this_player_input()
            self.update_screen()
        self.pg.quit()

    def listen_server(self):
        """
        this method must send (playable_rat_coords, finish_check) to server
        and receive (other_rat_coords, finish_check) from server
        """
        while True:
            self.this_rat.move()
            self.network.send(f"{self.this_rat.escaped};{self.this_rat.x},{self.this_rat.y}".encode(FORMAT))
            message = self.network.recv(BUFFSIZE).decode(FORMAT).split(';')
            if int(message[1]) == 1:
                self.running = False
            coords = rats_from_str(message[2])
            for i, coord in enumerate(coords):
                self.rats[i].update_maze(coord[0], coord[1])
            print("client console:", message)
