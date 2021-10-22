import math
import random

from service.service import Service
from settings import ROWS, COLS, AI_DIFFICULTY


class AI:
    def __init__(self):
        self.service = Service()

    def is_terminal_node(self, board):
        """
        Checks if the simulated game should or shouldn't continue
        :return: True or False
        """
        return self.service.check_win(board)[0] or len(self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board):
        """
        Searches for all valid locations in which a player can drop a piece
        :return: list
        """
        valid_locations = []
        for col in range(COLS):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def is_valid_location(self, board, col):
        return board[0][col] == 0

    def score_position(self, board, piece):
        """
        Generates the score for the specified player
        :param piece: 1 or 2
        :return: the generated score
        """
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROWS - 1, -1, -1):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLS - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROWS - 4, -1, -1):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROWS - 4, -1, -1):
            for c in range(COLS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(ROWS - 4, -1, -1):
            for c in range(COLS - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        """
        Generates the score for the specified move
        :param window: list of the diagonal/horizontal/vertical elements which will be checked
        :param piece: 1 or 2
        :return: the score
        """
        score = 0
        opp_piece = 1
        if piece == 1:
            opp_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def drop_piece(self, board, row, col, piece):
        """
        Drops a piece in the specified position
        """
        for i in range(ROWS):
            if board[i][col] == 0:
                row = i
        board[row][col] = piece

    def empty_board(self, board):
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != 0:
                    return False
        return True

    def minimax1(self, board, depth, alpha, beta, maximizingPlayer):
        """
        Starts the minimax algorithm
        :param board: current board
        :param depth: ai difficulty
        :param alpha beta: parameters used to fin the best score
        :param maximizingPlayer: True or False
        :return: ai's next
        """
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.service.check_win(board)[0] == 1:
                    return (None, random.randrange(-100000000000000, -99999999999000))
                elif self.service.check_win(board)[0] == 2:
                    return (None, 10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, 2))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                self.drop_piece(b_copy, 0, col, 2)
                new_score = self.minimax1(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                self.drop_piece(b_copy, 0, col, 1)
                new_score = self.minimax1(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def start(self, board, player):
        if self.empty_board(board):
            return random.randint(0, COLS - 1)

        return self.minimax1(board, AI_DIFFICULTY, -math.inf, math.inf, player)[0]
