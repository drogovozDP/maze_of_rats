import pygame as pg
import numpy as np
from game.consts import *
from game.graphic import Graphic


class Entity:
    def __init__(self, client, x, y, w, h, color):
        self.client = client
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.shape = self.create_shape()

    def create_shape(self):
        return lambda x, y: self.client.pg.Rect(x, y, self.w, self.h)

    def draw(self):
        self.client.pg.draw.rect(self.client.screen, self.color, self.shape(self.x, self.y))


class Wall(Entity):
    def __init__(self, client, x, y, w, h, color):
        super().__init__(client, x, y, w, h, color)


class Rat(Entity):
    def __init__(self, client, x, y, w, h, id, color):
        super().__init__(client, x, y, w, h, color)
        self.velocity = 10
        self.id = id

    def check_collision(self, dx, dy):
        for obj in self.client.game_objects:
            rx, ry, rw, rh = self.x + dx, self.y + dy, self.w, self.h
            ox, oy, ow, oh = obj.x, obj.y, obj.w, obj.h
            if rx < ox + ow and rx + rw > ox and ry < oy + oh and ry + rh > oy and self != obj:
                return
        self.x += dx
        self.y += dy

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

        self.this_player = this_player  # current player id
        self.rats = self.create_rats(players)  # create rats

        # create maze
        self.maze = self.create_maze_from_str(maze_str, maze_shape)
        self.graphic = Graphic(self)
        self.walls = self.create_walls()
        self.game_objects = self.walls + self.rats

    def create_walls(self):
        walls = []
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 0:
                    size = self.graphic.cell_size
                    walls.append(Wall(self, x * size, y * size, size, size, (155, 0, 55)))
        return walls

    def create_rats(self, players):
        rats = []
        for id, coords in players.items():
            rats.append(Rat(self, coords[0], coords[1], 30, 30, id, (255, 0, 0)))
        return rats

    def create_maze_from_str(self, maze_str, maze_shape):
        maze = np.array([int(cell) for cell in maze_str.split(', ')]).reshape(maze_shape)
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
