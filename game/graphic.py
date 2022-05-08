from game.consts import *


class Graphic:
    def __init__(self, client):
        self.client = client
        self.width = WIDTH
        self.height = HEIGHT
        self.set_max_xy()
        self.set_cell_wh()

    def draw_players(self):
        pass

    def draw_maze(self):
        for y, row in enumerate(self.client.maze):
            for x, cell in enumerate(row):
                self._draw_cell(x * self.cell_size, y * self.cell_size, clr=cell)

    def _draw_cell(self, x, y, clr):
        pad_x, pad_y = self.cell_pad
        self.client.pg.draw.rect(
            self.client.screen, COLOR[clr],
            self.client.pg.Rect(
                x + pad_x, y + pad_y,
                self.cell_size * 1.1, self.cell_size * 1.1
            )
        )

    def set_max_xy(self):
        self.max_y = len(self.client.maze)
        self.max_x = max([len(row) for row in self.client.maze])

    def set_cell_wh(self):
        """
        Cretas cell_size for cell width and height and cell_pad for padding
        """
        print(self.max_x, self.max_y)
        self.cell_size = min(self.height / self.max_y, self.width / self.max_x)
        self.cell_pad = ((self.width - self.max_x * self.cell_size) / 2, 0) \
            if self.max_x * self.width > self.max_y * self.height else \
            (0, (self.height - self.max_y * self.cell_size) / 2)
