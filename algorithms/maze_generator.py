import numpy as np
import random

"""
Maze must have shape = (2 * i + 1, 2 * j + 1), i, j = 2, 3, ...
"""

shape = (11, 11)


def generate_maze(shape, threshold=0.8):
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
    prev_poses = []
    maze[pos[0], pos[1]] = 0

    bypass = True
    while bypass:
        directions = get_directions()

        if len(directions) > 0:  # forward
            new_pos = random.choice(directions)
            prev_poses.append(pos)
            visit_cell(new_pos, pos)
            pos = new_pos.copy()
        else:  # backward
            pos = prev_poses.pop()

        if len(prev_poses) == 0:
            bypass = False

    # make noise to randomize paths
    def make_noise(shape, threshold):
        noise = np.ones(shape, dtype=int)
        global maze
        for y in range(noise.shape[0]):
            for x in range(noise.shape[1]):
                if random.random() > threshold:
                    noise[y, x] = 0
        noise[:, 0] = 1
        noise[:, -1] = 1
        noise[0, :] = 1
        noise[-1, :] = 1

        return noise

    noise = make_noise(shape, threshold)
    maze = maze * noise

    return maze
