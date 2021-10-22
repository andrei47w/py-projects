from settings import DIM, apple_count
import random


class Service:
    def __init__(self):
        self.matrix = [[0 for x in range(DIM)] for y in range(DIM)]
        self.direction = 'up'
        self.future_tail = DIM // 2, DIM // 2
        self.past_direction = -1, 0

    def validate_apple(self, x, y):
        if x - 1 > -1 and self.matrix[x - 1][y] != 0:
            return False
        if y - 1 > -1 and self.matrix[x][y - 1] != 0:
            return False
        if x + 1 < DIM and self.matrix[x + 1][y] != 0:
            return False
        if y + 1 < DIM and self.matrix[x][y + 1] != 0:
            return False
        if self.matrix[x][y] == 0:
            return True
        return False

    def place_apples(self, amount):
        for i in range(amount):

            while True:
                x = random.randrange(DIM)
                y = random.randrange(DIM)
                if self.validate_apple(x, y):
                    self.matrix[x][y] = 1
                    break

    def set_matrix(self, x, y, value):
        self.matrix[x][y] = value

    def place_snake(self):
        self.matrix[DIM // 2 - 1][DIM // 2] = 3
        self.matrix[DIM // 2][DIM // 2] = 2
        self.matrix[DIM // 2 + 1][DIM // 2] = 2

    def validate_move_input(self, amount):
        try:
            amount = int(amount)
            return True
        except:
            print('The amount of moves must be an int!')
            return False

    def get_direction(self):
        if self.direction == 'up':
            return -1, 0
        if self.direction == 'down':
            return 1, 0
        if self.direction == 'right':
            return 0, 1
        if self.direction == 'left':
            return 0, -1

    def get_tail(self):
        for i in range(DIM):
            for j in range(DIM):
                if self.storage()[i][j] == 2:
                    ok = 0
                    if not self.storage()[i - 1][j] in [0, 1]:
                        ok += 1
                    if not self.storage()[i + 1][j] in [0, 1]:
                        ok += 1
                    if not self.storage()[i][j - 1] in [0, 1]:
                        ok += 1
                    if not self.storage()[i][j + 1] in [0, 1]:
                        ok += 1
                    if ok == 1:
                        return i, j
        return self.future_tail

    def get_head(self):
        for i in range(DIM):
            for j in range(DIM):
                if self.storage()[i][j] == 3:
                    return i, j

    def validate_move(self, x, y):
        if x >= DIM or y >= DIM or x < 0 or y < 0 or self.storage()[x][y] == 2:
            raise ValueError('Game over!')
            return False
        return True

    def change_dir(self, dir):
        if (self.direction == 'up' and dir == 'down') or (self.direction == 'down' and dir == 'up') or (
                self.direction == 'right' and dir == 'left') or (self.direction == 'left' and dir == 'right'):
            print('Cannot change direction 180 degrees!')
        else:
            self.direction = dir

    def free_space(self):
        count = 0
        for i in range(DIM):
            for j in range(DIM):
                if self.storage()[i][j] == 1:
                    count += 1
        return count

    def move(self, amount):
        if not self.validate_move_input(amount):
            return
        amount = int(amount)

        if self.free_space() >= amount:
            amount = int(amount)
        else:
            amount = self.free_space()

        x, y = self.get_direction()
        past_x, past_y = self.past_direction

        xx, yy = self.future_tail
        self.future_tail = xx + past_x, yy + past_y

        for i in range(amount):
            self.past_direction = self.get_direction()
            head_x, head_y = self.get_head()
            if not self.validate_move(head_x + x, head_y + y):
                exit()

            tail_x, tail_y = self.get_tail()
            self.set_matrix(tail_x, tail_y, 0)
            self.set_matrix(head_x, head_y, 2)
            if self.storage()[head_x + x][head_y + y] == 1:
                self.set_matrix(tail_x, tail_y, 2)
                self.place_apples(1)

            self.set_matrix(head_x + x, head_y + y, 3)

    def storage(self):
        return self.matrix
