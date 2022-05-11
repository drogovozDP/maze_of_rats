from game.game_client import GameClient
import numpy as np
from algorithms.maze_generator import generate_maze

"""
maze will be look like:
maze = np.array([
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 4, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
])

this maze has shape=(5, 7), so str will be:
maze_str = '0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0'
all we have to do is use np.array().reshape(shape) and maze_str will be matrix again
"""


if __name__ == '__main__':
    # maze = np.array([
    #     [1, 1, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1],
    #     [1, 0, 4, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1],
    # ])
    shape = (51, 51)
    maze = generate_maze(shape, threshold=0.85)
    maze = maze.reshape(shape[0] * shape[1])
    maze = [str(cell) for cell in maze]
    maze_str = ''.join([cell + ', ' for i, cell in enumerate(maze) if i < len(maze) - 1]) + maze[-1]
    # print(''.join([a + ', ' for i, a in enumerate(['1', '0']) if i < len(['1', '0']) - 1] + ))
    GameClient(
        this_player=2,
        players={0: (1, 1), 1: (1, 2), 2: (1, 3)},
        maze_str=maze_str,
        maze_shape=shape
    ).run()