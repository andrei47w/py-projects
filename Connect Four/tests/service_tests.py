from tests.prepare_settings import replace
replace('settings.py', 'COLS = ', 'COLS = 16 #')
replace('settings.py', 'ROWS = ', 'ROWS = 8 #')

import unittest
import numpy
from service.service import Service
from settings import ROWS, COLS

class TestGame(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.board = self.service.board

    def test_availability(self):
        for row in range(ROWS - 1):
            self.board[row][0] = 1
        self.assertTrue(self.service.available_square(0, 0))
        self.board[7][0] = 2
        self.assertFalse(self.service.available_square(0, 0))
        self.assertFalse(self.service.available_square(3, 0))
        self.assertFalse(self.service.available_square(7, 0))
        self.assertFalse(self.service.available_square(5, 0))
        self.assertFalse(self.service.available_square(-20, 0))
        self.assertFalse(self.service.available_square(0, 20))
        self.assertFalse(self.service.available_square(0, -20))
        self.assertFalse(self.service.available_square(20, -20))

    def test_board_full(self):
        self.assertFalse(self.service.board_full())
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 1
        self.assertTrue(self.service.board_full())
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 2
        self.assertTrue(self.service.board_full())

    def reset_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 0

    def test_check_win(self):
        self.assertTrue(self.service.check_win(self.board)[0] == 0)
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 1
        self.assertTrue(self.service.check_win(self.board)[0] == 1)
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 2
        self.assertTrue(self.service.check_win(self.board)[0] == 2)

        self.reset_board()
        self.board[0][0] = self.board[0][1] = self.board[0][2] = self.board[0][3] = 1
        self.assertTrue(self.service.check_win(self.board)[0] == 1)
        self.board[0][0] = self.board[0][1] = self.board[0][2] = self.board[0][3] = 2
        self.assertTrue(self.service.check_win(self.board)[0] == 2)

        self.reset_board()
        self.board[0][0] = self.board[1][0] = self.board[2][0] = self.board[3][0] = 1
        self.assertTrue(self.service.check_win(self.board)[0] == 1)
        self.board[0][0] = self.board[1][0] = self.board[2][0] = self.board[3][0] = 2
        self.assertTrue(self.service.check_win(self.board)[0] == 2)

        self.reset_board()
        self.board[0][0] = self.board[1][1] = self.board[2][2] = self.board[3][3] = 1
        self.assertTrue(self.service.check_win(self.board)[0] == 1)
        self.board[0][0] = self.board[1][1] = self.board[2][2] = self.board[3][3] = 2
        self.assertTrue(self.service.check_win(self.board)[0] == 2)

        self.reset_board()
        self.board[3][0] = self.board[2][1] = self.board[1][2] = self.board[0][3] = 1
        self.assertTrue(self.service.check_win(self.board)[0] == 1)
        self.board[3][0] = self.board[2][1] = self.board[1][2] = self.board[0][3] = 2
        self.assertTrue(self.service.check_win(self.board)[0] == 2)

        self.assertTrue(type(self.service.storage()) == numpy.ndarray)

    def runTest(self):
        self.test_availability()
        self.test_board_full()
        self.test_check_win()

replace('settings.py', 'COLS = 16 #', 'COLS = ')
replace('settings.py', 'ROWS = 8 #', 'ROWS = ')
