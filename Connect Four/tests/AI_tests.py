from tests.prepare_settings import replace

replace('settings.py', 'COLS = ', 'COLS = 16 #')
replace('settings.py', 'ROWS = ', 'ROWS = 8 #')

import math
import unittest
import numpy as np
from AI.AI import AI
from service.service import Service
from settings import ROWS, COLS


class TestAI(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.board = self.service.board
        self.ai = AI()

    def test_is_terminal_node(self):
        # vertical win check
        self.board[ROWS - 1][COLS - 1] = 1
        self.board[ROWS - 1][COLS - 3] = 2
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 2][COLS - 3] = 2
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 3][COLS - 3] = 2
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 4][COLS - 3] = 2
        self.assertTrue(self.ai.is_terminal_node(self.board))

        # horizontal win check
        self.board[ROWS - 4][COLS - 3] = 0
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 1][COLS - 4] = 2
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 1][COLS - 5] = 2
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 1][COLS - 6] = 2
        self.assertTrue(self.ai.is_terminal_node(self.board))

        # right diagonal win check
        self.board[ROWS - 1][COLS - 6] = 0
        self.board[ROWS - 1][COLS - 1] = 1
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 2][COLS - 2] = 1
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 3][COLS - 3] = 1
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 4][COLS - 4] = 1
        self.assertTrue(self.ai.is_terminal_node(self.board))

        # left diagonal win check
        self.board[ROWS - 4][COLS - 4] = 0
        self.board[ROWS - 1][COLS - 4] = 1
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 2][COLS - 3] = 1
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 3][COLS - 2] = 1
        self.assertFalse(self.ai.is_terminal_node(self.board))
        self.board[ROWS - 4][COLS - 1] = 1
        self.assertTrue(self.ai.is_terminal_node(self.board))

        # empty board
        self.board = np.zeros((ROWS, COLS))
        self.assertFalse(self.ai.is_terminal_node(self.board))

        # full board
        for col in range(COLS):
            for row in range(ROWS):
                self.board[row][col] = 1
        self.assertTrue(self.ai.is_terminal_node(self.board))

    def test_minimax(self):
        self.board[ROWS - 1][COLS - 2] = 2
        self.board[ROWS - 1][COLS - 3] = 2
        self.board[ROWS - 1][COLS - 4] = 2
        self.assertTrue(self.ai.minimax1(self.board, 2, -math.inf, math.inf, True)[0] == COLS - 5)

        self.board[ROWS - 1][COLS - 2] = 1
        self.board[ROWS - 1][COLS - 3] = 1
        self.board[ROWS - 1][COLS - 4] = 1
        self.assertTrue(self.ai.minimax1(self.board, 1, -math.inf, math.inf, True)[0] == COLS - 5)

        self.board[ROWS - 1][COLS - 1] = 2
        self.board[ROWS - 2][COLS - 1] = 2
        self.board[ROWS - 3][COLS - 1] = 2
        self.assertTrue(self.ai.minimax1(self.board, 2, -math.inf, math.inf, True)[0] == COLS - 1)

        self.board = np.zeros((ROWS, COLS))
        self.board[ROWS - 1][COLS - 1] = 1
        self.board[ROWS - 2][COLS - 1] = 1
        self.board[ROWS - 3][COLS - 1] = 1
        self.assertTrue(self.ai.minimax1(self.board, 1, -math.inf, math.inf, True)[0] == COLS - 1)

    def runTest(self):
        self.test_minimax()
        self.test_is_terminal_node()


replace('settings.py', 'COLS = 16 #', 'COLS = ')
replace('settings.py', 'ROWS = 8 #', 'ROWS = ')
