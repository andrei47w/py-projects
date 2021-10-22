import sys

import pygame

from AI.AI import AI
from service.service import Service
from settings import WIDTH, HEIGHT, ROWS, COLS, FG, BG, RED, BLUE, SECRET_BUTTON, piece_1_sound, piece_2_sound, \
    win_sound, click_sound, VOLUME, erase_sound


class Game:
    def __init__(self):
        self.service = Service()
        self.ai = AI()

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Connect four')
        screen.fill(BG)
        self.screen = screen
        self.draw_menu()

    def play_sound(self, sound):
        pygame.mixer.music.load('sound_files//' + sound)
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.play(0)

    def draw_text(self):
        font = pygame.font.SysFont('Console', 30, bold=True)
        pygame.draw.circle(self.screen, RED, (168, 52), 18, 18)
        pygame.draw.circle(self.screen, BLUE, (368, 52), 18, 18)

        self.screen.blit(font.render('Player', True, RED), (31, 37))
        self.screen.blit(font.render('1', True, BG), (160, 37))

        self.screen.blit(font.render('Player', True, BLUE), (231, 37))
        self.screen.blit(font.render('2', True, BG), (360, 37))

        font = pygame.font.SysFont('Console', 25, bold=False)
        self.screen.blit(font.render("Press   to reset board", True, FG), (464, 50))
        self.screen.blit(font.render("Press     to open menu", True, FG), (464, 20))
        font = pygame.font.SysFont('Console', 25, bold=True)
        self.screen.blit(font.render("r", True, FG), (553, 50))
        self.screen.blit(font.render("esc", True, FG), (553, 20))

        pygame.display.update()

    def draw_text_CPU(self):
        font = pygame.font.SysFont('Console', 30, bold=True)
        pygame.draw.circle(self.screen, RED, (168, 52), 18, 18)
        pygame.draw.circle(self.screen, BLUE, (368, 52), 18, 18)

        self.screen.blit(font.render('Player', True, RED), (31, 37))

        self.screen.blit(font.render('CPU', True, BLUE), (286, 37))

        font = pygame.font.SysFont('Console', 25, bold=False)
        self.screen.blit(font.render("Press   to reset board", True, FG), (464, 50))
        self.screen.blit(font.render("Press     to open menu", True, FG), (464, 20))
        font = pygame.font.SysFont('Console', 25, bold=True)
        self.screen.blit(font.render("r", True, FG), (553, 50))
        self.screen.blit(font.render("esc", True, FG), (553, 20))

        pygame.display.update()

    def draw_start(self):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.circle(self.screen, FG, (int((col + 1) * 50 + 30) - 5, int((row + 1) * 50 + 79) - 5), 6, 6)
                pygame.draw.circle(self.screen, FG, (int((col + 1) * 50 + 30) - 48, int((row + 1) * 50 + 79) - 48), 6,
                                   6)
                pygame.draw.circle(self.screen, FG, (int((col + 1) * 50 + 30) - 48, int((row + 1) * 50 + 79) - 5), 6, 6)
                pygame.draw.circle(self.screen, FG, (int((col + 1) * 50 + 30) - 5, int((row + 1) * 50 + 79) - 48), 6, 6)
                pygame.draw.circle(self.screen, FG, (int(col * 50 + 54), int(row * 50 + 103)), 28, 6)
        row = 77
        col = 28
        for i in range(ROWS + 1):
            pygame.draw.line(self.screen, FG, (26, row), (col + 50 * COLS + 3, row), 6)
            row += 50
        for i in range(COLS + 1):
            pygame.draw.line(self.screen, FG, (col, 77), (col, row - 50), 6)
            col += 50

        pygame.display.update()


    def draw_figures(self):
        self.play_sound(piece_1_sound)
        for row in range(ROWS):
            for col in range(COLS):
                if self.service.board()[row][col] == 1:
                    pygame.draw.circle(self.screen, RED, (int(col * 50 + 54), int(row * 50 + 103)), 22, 22)
                elif self.service.board()[row][col] == 2:
                    pygame.draw.circle(self.screen, BLUE, (int(col * 50 + 54), int(row * 50 + 103)), 22, 22)

    def draw_animation(self, row, col, player):
        self.play_sound(piece_2_sound)

        row = int(row * 50 + 103)
        col = int(col * 50 + 54)
        final_line = row - 1
        if player == 1:
            COLOR = RED
        else:
            COLOR = BLUE

        # Dropping animation
        for line in range(row, ROWS * 50 + 53, 5):
            board_row = (line - 103) / 50
            board_col = (col - 54) / 50
            if line >= ROWS * 50 + 35:
                final_line = line + 5
            else:
                final_line = line
            if (board_row).is_integer() and self.service.board()[int(board_row) + 1][int(board_col)] != 0:
                break
            pygame.draw.circle(self.screen, COLOR, (col, line), 20, 20)
            self.draw_start()
            pygame.time.wait(2)
            pygame.draw.circle(self.screen, BG, (col, line), 20, 20)

        final_line -= 2
        # Bounce animation
        pygame.draw.ellipse(self.screen, COLOR, (col - 19, final_line - 11, 40, 35))
        self.draw_start()
        pygame.time.wait(20)
        pygame.draw.ellipse(self.screen, BG, (col - 19, final_line - 11, 40, 35))

        pygame.draw.ellipse(self.screen, COLOR, (col - 19, final_line - 3, 40, 26))
        self.draw_start()
        pygame.time.wait(20)
        pygame.draw.ellipse(self.screen, BG, (col - 19, final_line - 3, 40, 26))

        pygame.draw.ellipse(self.screen, COLOR, (col - 19, final_line - 7, 40, 32))
        self.draw_start()
        pygame.time.wait(20)
        pygame.draw.ellipse(self.screen, BG, (col - 19, final_line - 7, 40, 32))

        pygame.draw.ellipse(self.screen, COLOR, (col - 19, final_line - 10, 40, 35))
        self.draw_start()
        pygame.time.wait(20)
        pygame.draw.ellipse(self.screen, BG, (col - 19, final_line - 10, 40, 35))

        self.draw_start()

    def draw_win(self):
        player, col2, row2, col, row = self.service.check_win(self.service.board())
        if player == 1:
            COLOR = RED
        else:
            COLOR = BLUE
        row = row * 50 + 53
        col = col * 50 + 104

        i = col - 2
        j = row
        while i in range(col - 2, col + col2 * 50 - 1) and (
                j in range(row, row + row2 * 50 + 1) or j in range(row + row2 * 50 + 1, row + 1)):
            pygame.draw.line(self.screen, COLOR, (row, col - 2), (j, i), 42)
            pygame.display.update()
            pygame.time.wait(17)
            if col2 < 0:
                i -= 10
            if col2 > 0:
                i += 10
            if row2 < 0:
                j -= 10
            if row2 > 0:
                j += 10
        pygame.draw.line(self.screen, COLOR, (row, col - 2), (row + row2 * 50, col + col2 * 50 - 2), 42)

        self.play_sound(win_sound)
        # pygame.time.wait(300)

        pygame.draw.circle(self.screen, BG, (WIDTH // 2, HEIGHT // 2), 120, 120)
        pygame.draw.circle(self.screen, COLOR, (WIDTH // 2, HEIGHT // 2), 100, 100)

        font = pygame.font.SysFont('Console', 80, bold=True)
        self.screen.blit(font.render('WIN', True, BG), (WIDTH // 2 - 71, HEIGHT // 2 - 40))
        pygame.display.update()

    def draw_draw(self):
        self.play_sound(win_sound)
        pygame.draw.circle(self.screen, BG, (429, 240), 120, 120)
        pygame.draw.circle(self.screen, FG, (429, 240), 100, 100)

        font = pygame.font.SysFont('Console', 70, bold=True)
        self.screen.blit(font.render('DRAW', True, BG), (344, 200))
        pygame.display.update()

    def mark_square(self, row, col):
        new_row = row
        for i in range(ROWS):
            if self.service.board()[i][col] == 0:
                new_row = i
        return new_row

    def restart(self):
        self.play_sound(erase_sound)
        pygame.time.wait(100)
        self.screen.fill(BG)
        self.draw_start()
        self.draw_text()

    def restart_CPU(self):
        self.play_sound(erase_sound)
        pygame.time.wait(100)
        self.screen.fill(BG)
        self.draw_start()
        self.draw_text_CPU()

    def draw_menu(self):
        self.play_sound(click_sound)

        self.screen.fill(BG)
        font = pygame.font.SysFont('Console', 80, bold=True)
        self.screen.blit(font.render('C NNECT F UR', True, FG), (140, 50))

        pygame.draw.line(self.screen, RED, (255, 303), (555, 303), 100)
        pygame.draw.line(self.screen, BG, (264, 248), (245, 268), 20)
        pygame.draw.line(self.screen, BG, (545, 248), (564, 268), 20)
        pygame.draw.circle(self.screen, RED, (270, 269), 15, 15)
        pygame.draw.circle(self.screen, RED, (541, 269), 15, 15)

        pygame.draw.line(self.screen, BLUE, (255, 403), (555, 403), 100)
        pygame.draw.line(self.screen, BG, (245, 438), (264, 458), 20)
        pygame.draw.line(self.screen, BG, (545, 458), (564, 438), 20)
        pygame.draw.circle(self.screen, BLUE, (270, 439), 15, 15)
        pygame.draw.circle(self.screen, BLUE, (541, 439), 15, 15)

        if SECRET_BUTTON:
            pygame.draw.line(self.screen, FG, (255, 480), (555, 480), 100)
            pygame.draw.line(self.screen, BLUE, (255, 403), (555, 403), 100)

        font = pygame.font.SysFont('Console', 50, bold=True)
        self.screen.blit(font.render('1 Player', True, BG), (285, 280))
        self.screen.blit(font.render('2 Players', True, BG), (271, 380))

        pygame.draw.circle(self.screen, RED, (212, 94), 24, 24)
        pygame.draw.circle(self.screen, BLUE, (597, 94), 24, 24)

        pygame.display.update()

    def start_2players(self):
        """
        Starts playing the 2 Players option
        """
        self.draw_start()
        self.draw_text()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_y = (int(event.pos[0]) - 28) // 50
                    click_x = (int(event.pos[1]) - 77) // 50

                    if self.service.available_square(click_x, click_y):
                        if self.service.player == 1:
                            self.draw_animation(click_x, click_y, 1)
                            click_x = self.mark_square(click_x, click_y)
                            self.service.board()[click_x][click_y] = 1
                            self.service.player = 2
                        elif self.service.player == 2:
                            self.draw_animation(click_x, click_y, 2)
                            click_x = self.mark_square(click_x, click_y)
                            self.service.board()[click_x][click_y] = 2
                            self.service.player = 1
                        self.draw_figures()
                        if self.service.check_win(self.service.board())[0] != 0:
                            self.draw_win()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.restart()
                        if self.service.board_full():
                            self.draw_draw()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.restart()
                        # print(self.service.board())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.service.empty_board()
                        self.restart()
                    if event.key == pygame.K_ESCAPE:
                        game = Game()
                        game.start()
            pygame.display.update()

    def start_1player(self):
        """
        Starts playing the 1 Player option (against the AI)
        """
        self.draw_start()
        self.draw_text_CPU()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_y = (int(event.pos[0]) - 28) // 50
                    click_x = (int(event.pos[1]) - 77) // 50

                    if self.service.available_square(click_x, click_y):
                        self.draw_animation(click_x, click_y, 1)
                        click_x = self.mark_square(click_x, click_y)
                        self.service.board()[click_x][click_y] = 1
                        self.draw_figures()
                        pygame.display.update()
                        if self.service.check_win(self.service.board())[0] == 1.0:
                            self.draw_win()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.restart_CPU()

                        click_y, click_x = self.ai.start(self.service.board(), True), 0
                        if self.service.available_square(click_x, click_y):
                            self.draw_animation(click_x, click_y, 2)
                            click_x = self.mark_square(click_x, click_y)
                            self.service.board()[click_x][click_y] = 2
                            self.draw_figures()
                            pygame.display.update()
                        if self.service.check_win(self.service.board())[0] == 2.0:
                            self.draw_win()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.restart_CPU()

                        if self.service.board_full():
                            self.draw_draw()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.restart_CPU()
                        # print(self.service.board())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.service.empty_board()
                        self.restart_CPU()
                    if event.key == pygame.K_ESCAPE:
                        game = Game()
                        game.start()
            pygame.display.update()

    def start_0player(self):
        self.draw_start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_y, click_x = self.ai.start(self.service.board(), False), 0

                    if self.service.available_square(click_x, click_y):
                        self.draw_animation(click_x, click_y, 1)
                        click_x = self.mark_square(click_x, click_y)
                        self.service.board()[click_x][click_y] = 1
                        self.draw_figures()
                        pygame.display.update()
                        if self.service.check_win(self.service.board())[0] == 1.0:
                            self.draw_win()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.screen.fill(BG)
                            self.draw_start()

                        click_y, click_x = self.ai.start(self.service.board(), False), 0
                        if self.service.available_square(click_x, click_y):
                            self.draw_animation(click_x, click_y, 2)
                            click_x = self.mark_square(click_x, click_y)
                            self.service.board()[click_x][click_y] = 2
                            self.draw_figures()
                            pygame.display.update()
                        if self.service.check_win(self.service.board())[0] == 2.0:
                            self.draw_win()
                            pygame.time.wait(2000)
                            self.screen.fill(BG)
                            self.service.empty_board()
                            self.draw_start()

                        if self.service.board_full():
                            self.draw_draw()
                            pygame.time.wait(2000)
                            self.service.empty_board()
                            self.screen.fill(BG)
                            self.draw_start()
                        # print(self.service.board())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.screen.fill(BG)
                        self.draw_start()
                        self.service.empty_board()
                    if event.key == pygame.K_ESCAPE:
                        game = Game()
                        game.start()
            pygame.display.update()

    # START FUNCTION

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_x = event.pos[0]
                    click_y = event.pos[1]

                    # 1 Player button
                    if 250 < click_x < 555 and 253 < click_y < 353:
                        self.play_sound(click_sound)
                        self.screen.fill(BG)
                        self.start_1player()

                    # 2 Player button
                    if 250 < click_x < 555 and 353 < click_y < 453:
                        self.play_sound(click_sound)
                        self.screen.fill(BG)
                        self.start_2players()

                    # Super secret button
                    if 250 < click_x < 555 and 453 < click_y < 553 and SECRET_BUTTON:
                        self.play_sound(click_sound)
                        self.screen.fill(BG)
                        self.start_0player()
