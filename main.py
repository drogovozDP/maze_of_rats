from game.game_client import GameClient

"""
maze will be look like:
maze = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 2, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
])

this maze has shape=(5, 7), so str will be:
maze_str = '0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0'
all we have to do is use np.array().reshape(shape) and maze_str will be matrix again
"""


if __name__ == '__main__':
    GameClient(
        this_player=0,
        players={0: (250, 150), 1: (400, 150), 2: (150, 400)},
        maze_str="0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0",
        maze_shape=(5, 7)
    ).run()