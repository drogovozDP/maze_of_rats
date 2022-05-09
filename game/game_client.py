import pygame as pg
import numpy as np
from game.consts import *
from game.graphic import Graphic
from _thread import *


class Entity:
    def __init__(self, client, x, y, color):
        self.client = client
        self.x = x
        self.y = y
        self.color = color
        self.size = self.client.graphic.cell_size

    def draw(self):
        x = self.x * self.size
        y = self.y * self.size
        self.client.pg.draw.rect(self.client.screen, self.color,
                                 self.client.pg.Rect(x, y, self.size, self.size))


class Rat(Entity):
    def __init__(self, client, x, y, id, color):
        super().__init__(client, x, y, color)
        self.velocity = 1
        self.maze_vision = self.client.maze.copy()
        self.id = id

    def create_vision(self):
        maze_shape = self.client.maze.shape()
        maze_vision = np.full(maze_shape, 2)
        return maze_vision

    def update_maze(self, x, y):
        self.client.maze[self.y, self.x] = FLOOR
        self.client.maze[y, x] = RAT
        self.x = x
        self.y = y
        print(self.client.maze)

    def check_collision(self, dx, dy):
        x = self.x + dx
        y = self.y + dy
        cell = self.client.maze[y, x]
        print(x, y, self.client.maze[y, x])
        if cell != FLOOR and cell != FINISH:
            return
        self.update_maze(x, y)

    def move(self, direction):
        if direction == 'up':
            self.check_collision(0, -self.velocity)
        elif direction == 'down':
            self.check_collision(0, self.velocity)
        elif direction == 'left':
            self.check_collision(-self.velocity, 0)
        elif direction == 'right':
            self.check_collision(self.velocity, 0)


class GameClient:
    """
    This class takes dict of players {id: coords}, current player's id, string
    of maze and shape for it.
    """

    def __init__(self, this_player, players, maze_str, maze_shape):
        # pygame standard init
        self.pg = pg
        self.screen = self.pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = self.pg.time.Clock()
        self.FPS = 60
        self.running = True

        # create maze
        self.maze = self.create_maze_from_str(maze_str, maze_shape, players)
        self.graphic = Graphic(self)

        self.this_player = this_player  # current player id
        self.rats = self.create_rats(players)  # create rats

    def create_rats(self, players):
        rats = []
        for id, coords in players.items():
            rats.append(Rat(self, coords[0], coords[1], id, (255, 0, 0)))
        return rats

    def create_maze_from_str(self, maze_str, maze_shape, players):
        maze = np.array([int(cell) for cell in maze_str.split(', ')]).reshape(maze_shape)
        for plr, val in players.items():
            maze[val[1], val[0]] = RAT
        print(maze)
        return maze

    def this_player_input(self):
        for event in self.pg.event.get():
            if event.type == self.pg.QUIT:
                self.running = False
        keys = self.pg.key.get_pressed()
        if keys[self.pg.K_UP]:
            self.rats[self.this_player].move('up')
        if keys[self.pg.K_DOWN]:
            self.rats[self.this_player].move('down')
        if keys[self.pg.K_LEFT]:
            self.rats[self.this_player].move('left')
        if keys[self.pg.K_RIGHT]:
            self.rats[self.this_player].move('right')

    def update_screen(self):
        self.clock.tick(self.FPS)
        self.screen.fill(COLOR['bg'])
        self.graphic.draw_environment()
        self.pg.display.update()

    def run(self):
        while self.running:
            self.this_player_input()
            self.update_screen()