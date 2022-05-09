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

    def visit_cell(new_pos, old_pos):
        ny, nx = new_pos
        oy, ox = old_pos
        dy, dx = (ny - oy) // 2, (nx - ox) // 2
        print(f"old: x={ox}, y={oy}")
        print(f"new: x={nx}, y={ny}")
        print("-----------------")
        maze[ny, nx], maze[oy + dy, ox + dx] = 0, 0

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
    maze[pos[0], pos[1]] = 0

    iter = 0
    while True:
        directions = get_directions()
        print(f"Iter={iter} ||| " + "=" * 50)
        print(maze)
        print(f"directions: {directions}")

        new_pos = random.choice(directions)

        print(f"random choice: {new_pos}")

        prev_list.append(pos)
        visit_cell(new_pos, pos)
        pos = new_pos.copy()

        print("=" * 50)

        if len(prev_list) == 0 or iter == 5:
            break

    # maze[shape[0] // 2, shape[1] // 2] = 4
    return maze

generate_maze(shape)
# print(generate_maze(shape).shape)