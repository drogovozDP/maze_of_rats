"""
0 - wall
1 - floor
2 - blind cell
3 - rat
4 - finish/escape/cheese
"""
import os
from pathlib import Path

FLOOR = 0
WALL = 1
BLIND = 2
RAT = 3
FINISH = 4
WAS_HERE = 5

COLOR = {
    'bg': (0, 0, 0),
    WALL: (223, 131, 34),
    FLOOR: (50, 50, 50),
    BLIND: (10, 10, 10),
    RAT: (50, 50, 50),
    FINISH: (155, 155, 0)
}

WIDTH = 800
HEIGHT = 600

SPRITE_DIR = Path(os.getcwd()) / 'sprites'
