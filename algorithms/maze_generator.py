import numpy as np
import random

"""
Maze must have shape = (2 * i + 1, 2 * j + 1), i, j = 2, 3, ...
"""

shape = (7, 7)


def generate_maze(shape):
    maze = np.full(shape, 2)
    # generating walls
    for x in range(0, maze.shape[1], 2):
        maze[:, x] = 1
    for y in range(0, maze.shape[0], 2):
        maze[y, :] = 1

    def check_neighbor_cell(direction):
        y, x = pos
        if direction == 'up':
            y -= 2
        elif direction == 'down':
            y += 2
        elif direction == 'left':
            x -= 2
        elif direction == 'right':
            x += 2
        if y <= 0 or x <= 0 or y >= maze.shape[0] - 1 or x >= maze.shape[1] - 1:
            return False
        return True if maze[y, x] == 2 else False

    def visit_cell(shape):
        y, x = shape
        maze[y, x] = 0

    def get_directions():
        directions = []
        if check_neighbor_cell('up'):
            directions.append([pos[0] - 2, pos[1]])
        if check_neighbor_cell('down'):
            directions.append([pos[0] + 2, pos[1]])
        if check_neighbor_cell('left'):
            directions.append([pos[0], pos[1] - 2])
        if check_neighbor_cell('right'):
            directions.append([pos[0], pos[1] + 2])
        return directions

    pos = [1, 1]
    prev_list = []
    visit_cell(pos)

    iter = 0
    while True:
        # check_neighbors()
        directions = get_directions()
        new_pos = random.choice(directions)
        print(f"Iter={iter} ||| " + "=" * 50)
        print(maze)
        print(f"directions: {directions}")
        print(f"random choice: {new_pos}")
        print("=" * 50)
        # prev_list.append(pos)

        if len(prev_list) == 0:
            break


    # maze[shape[0] // 2, shape[1] // 2] = 4
    return maze

generate_maze(shape)
# print(generate_maze(shape).shape)