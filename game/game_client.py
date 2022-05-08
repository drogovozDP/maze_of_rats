import pygame as pg
import numpy as np
from game.consts import *
from game.graphic import Graphic


class Rat:
    def __init__(self, client, x, y, id):
        self.client = client
        self.x = x
        self.y = y
        self.id = id
        self.rat = self.create_shape()

    def create_shape(self):
        return lambda x, y: self.client.pg.Rect(x, y, 30, 30)

    def move(self):
        pass

    def draw(self):
        self.client.pg.draw.rect(self.client.screen, (255, 0, 0), self.rat(self.x, self.y))


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

    def create_rats(self, players):
        rats = []
        for id, coords in players.items():
            rats.append(Rat(self, coords[0], coords[1], id))
        return rats

    def create_maze_from_str(self, maze_str, maze_shape):
        maze = np.array([int(cell) for cell in maze_str.split(', ')]).reshape(maze_shape)
        print(maze)
        return maze

    def this_player_input(self):
        for event in self.pg.event.get():
            if event.type == self.pg.QUIT:
                self.running = False
        keys = self.pg.key.get_pressed()
        if keys[self.pg.K_UP]:
            pass
        if keys[self.pg.K_DOWN]:
            pass
        if keys[self.pg.K_LEFT]:
            pass
        if keys[self.pg.K_RIGHT]:
            pass

    def update_screen(self):
        self.clock.tick(self.FPS)
        self.screen.fill(COLOR['bg'])
        self.graphic.draw_environment()
        self.pg.display.update()

    def run(self):
        while self.running:
            self.this_player_input()
            self.update_screen()


