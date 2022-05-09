"""
0 - wall
1 - floor
2 - blind cell
3 - rat
4 - finish/escape/cheese
"""

FLOOR = 0
WALL = 1
BLIND = 2
RAT = 3
FINISH = 4

COLOR = {
    'bg': (0, 0, 0),
    WALL: (223, 131, 34),
    FLOOR: (50, 50, 50),
    BLIND: (150, 150, 150),
    RAT: (155, 0, 155),
    FINISH: (155, 155, 0)
}

WIDTH = 800
HEIGHT = 600
