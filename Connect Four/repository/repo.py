import numpy as np

from settings import ROWS, COLS


class Repo:
    def __init__(self):
        self.game_board = np.zeros((ROWS, COLS))

    def board(self):
        return self.game_board

    def empty_board(self):
        self.game_board = np.zeros((ROWS, COLS))
