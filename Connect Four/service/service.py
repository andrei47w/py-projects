from repository.repo import Repo
from settings import ROWS, COLS


class Service:
    def __init__(self):
        self.repo = Repo()
        self.player = 1

    def board(self):
        return self.repo.board()

    def empty_board(self):
        """
        Empties board
        """
        self.repo.empty_board()

    def available_square(self, row, col):
        """
        Checks if the position (row, col) is free on the board
        :param row: int
        :param col: int
        :return: True or False
        """
        try:
            col = int(col)
        except:
            return False
        if -1 < col < COLS and -1 < row < ROWS:
            for i in range(row, ROWS):
                if self.board()[i][col] == 0:
                    return True
        return False

    def board_full(self):
        """
        Checks if the board is full
        :return: True or False
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.board()[row][col] == 0:
                    return False
        return True

    def check_win(self, board):
        """
        Checks if any player has won
            -if there is a winner, returns the player who won, type of win and winning move
            -if there is no winner, returns only 0 values
        :param board: current board
        :return: winning_player, x_type, y_type, x, y
        """
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != 0:
                    ok = 0
                    row2 = 0
                    col2 = 0
                    if row + 3 < ROWS and board[row + 3][col] == board[row + 2][col] == board[row + 1][col] == \
                            board[row][col]:
                        ok = 1
                        row2 = 3
                        col2 = 0
                    elif col + 3 < COLS and board[row][col + 3] == board[row][col + 2] == board[row][col + 1] == \
                            board[row][col]:
                        ok = 1
                        row2 = 0
                        col2 = 3
                    elif row + 3 < ROWS and col + 3 < COLS and board[row + 3][col + 3] == board[row + 2][
                        col + 2] == board[row + 1][col + 1] == board[row][col]:
                        ok = 1
                        row2 = 3
                        col2 = 3
                    elif row + 3 < ROWS and col - 3 > -1 and board[row + 3][col - 3] == board[row + 2][col - 2] == \
                            board[row + 1][col - 1] == board[row][col]:
                        ok = 1
                        row2 = 3
                        col2 = -3

                    if ok != 0:
                        return board[row][col], row2, col2, row, col

        return 0, 0, 0, 0, 0
