import pygame as pg
import numpy as np
from game.consts import *
from game.graphic import Graphic


class GameClient:
    """
    This class takes dict of players {id: coords}, current player's id, string
    of maze and shape for it. These arguments transfer to GameEngine class, which will compute
    and visualize to user.
    """
    def __init__(self, this_player, players, maze_str, maze_shape):
        self.this_player = this_player
        self.players = players
        self.pg = pg
        self.screen = self.pg.display.set_mode((WIDTH, HEIGHT))
        self.maze = self.create_maze_from_str(maze_str, maze_shape)
        self.graphic = Graphic(self)
        self.clock = self.pg.time.Clock()
        self.FPS = 60
        self.running = True

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
        self.graphic.draw_maze()
        self.pg.display.update()

    def run(self):
        while self.running:
            self.this_player_input()
            self.update_screen()


