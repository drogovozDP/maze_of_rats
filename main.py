from game.game_client import GameClient

"""
maze will be look like:
maze = [
    0000000
    0111110
    0100010
    0121110
    0000000
]

this maze has shape=(5, 7), so str will be:
maze_str = '00000000111110010001001211100000000'
all we have to do is use np.array().reshape(shape) and maze_str will be matrix again
"""


if __name__ == '__main__':
    GameClient(
        this_player=0,
        players={0: (50, 50), 1: (400, 50), 2: (50, 400)},
        maze_str="00000000111110010001001211100000000",
        maze_shape=(5, 7)
    ).run()