from service import Service
from settings import DIM, apple_count


class UI:
    def __init__(self):
        self.service = Service()

    def place_apples(self):
        self.service.place_apples(apple_count)

    def place_snake(self):
        self.service.place_snake()

    def print(self):
        matrix = self.service.storage()
        for i in range(DIM):
            for j in range(DIM):
                print('+---', end='')
            print('+')

            for j in range(DIM):
                if j == 0:
                    print('| ', end='')
                if matrix[i][j] == 1:
                    print('. | ', end='')
                elif matrix[i][j] == 0:
                    print('  | ', end='')
                elif matrix[i][j] == 2:
                    print('+ | ', end='')
                else:
                    print('* | ', end='')
            print()
        for j in range(DIM):
            print('+---', end='')
        print('+')

    def move(self, cmd):
        if cmd == '':
            self.service.move(1)
        else:
            self.service.move(cmd)

    def change_up(self):
        self.service.change_dir('up')

    def change_down(self):
        self.service.change_dir('down')

    def change_left(self):
        self.service.change_dir('left')

    def change_right(self):
        self.service.change_dir('right')

    def start(self):
        try:
            self.place_snake()
            self.place_apples()
            self.print()
            while True:
                cmd = input()
                if cmd[:4] == 'move':
                    self.move(cmd[5:])
                elif cmd[:2] == 'up':
                    self.change_up()
                elif cmd[:4] == 'down':
                    self.change_down()
                elif cmd[:4] == 'left':
                    self.change_left()
                elif cmd[:5] == 'right':
                    self.change_right()
                else:
                    print('Invalid input!')
                self.print()
        except Exception as e:
            print(str(e))
