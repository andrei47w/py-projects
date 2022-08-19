import time
from copy import deepcopy

import pygame
from pygame import font
from pygame.locals import *

from utils import *


def initPygame(dimension):
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with ACO")
    screen = pygame.display.set_mode(dimension)
    screen.fill(Utils.WHITE)
    return screen


def closePygame():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


def moveDrone(screen, map, path, battery, speed=0.25):
    drona = pygame.transform.scale(pygame.image.load("drona.png"), (Utils.COLUMN_SIZE, Utils.ROW_SIZE))
    brick = pygame.Surface((Utils.COLUMN_SIZE, Utils.ROW_SIZE))
    brick.fill(Utils.GREEN)
    sighted_cell = pygame.Surface((Utils.COLUMN_SIZE, Utils.ROW_SIZE))
    sighted_cell.fill(Utils.RED)
    sensor = pygame.transform.scale(pygame.image.load("sensor.png"), (Utils.COLUMN_SIZE, Utils.ROW_SIZE))
    battery += 1
    running = True
    map.surface[path[0][0]][path[0][1]] = 0
    for cell_i in range(len(path)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not running:
            break
        screen.blit(image(map), (0, 0))
        battery -= path[cell_i][2] + 1

        for j in range(cell_i + 1):
            screen.blit(brick, (path[j][1] * Utils.COLUMN_SIZE, path[j][0] * Utils.ROW_SIZE))
        for cell in path[:cell_i + 1]:
            if map.surface[cell[0]][cell[1]] == 1:
                i = cell[0]
                j = cell[1]
                neighbours = [[i, j], [i, j], [i, j], [i, j]]
                for _ in range(cell[2]):
                    for direction_index in range(len(Utils.DIRECTIONS)):
                        new_neighbour = deepcopy(neighbours[direction_index])
                        new_neighbour[0] += Utils.DIRECTIONS[direction_index][0]
                        new_neighbour[1] += Utils.DIRECTIONS[direction_index][1]
                        if 0 <= new_neighbour[0] < map.n and 0 <= new_neighbour[1] < map.m:
                            if map.surface[new_neighbour[0]][new_neighbour[1]] != 2:
                                neighbours[direction_index] = new_neighbour
                                screen.blit(sighted_cell,
                                            (new_neighbour[1] * Utils.COLUMN_SIZE, new_neighbour[0] * Utils.ROW_SIZE))

        pygame.font.init()
        font = pygame.font.SysFont("Grobold", 25)

        for i in range(map.n):
            for j in range(map.m):
                if map.surface[i][j] == 1:
                    screen.blit(sensor, (j * Utils.COLUMN_SIZE, i * Utils.ROW_SIZE))

                    for cell in path:
                        if cell[0] == i and cell[1] == j:
                            text = font.render(str(cell[2]), True, Utils.BLACK)
                            textRect = text.get_rect()
                            textRect.center = (j * Utils.COLUMN_SIZE + 15, i * Utils.ROW_SIZE + 15)
                            screen.blit(text, textRect)
                            break

        screen.blit(drona, (path[cell_i][1] * Utils.COLUMN_SIZE, path[cell_i][0] * Utils.ROW_SIZE))
        pygame.display.flip()
        time.sleep(speed)


def image(current_map, colour=Utils.BLUE, background=Utils.WHITE):
    imagine = pygame.Surface((current_map.m * Utils.COLUMN_SIZE, current_map.n * Utils.ROW_SIZE))
    brick = pygame.Surface((Utils.COLUMN_SIZE, Utils.ROW_SIZE))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(current_map.n):
        for j in range(current_map.m):
            if current_map.surface[i][j] == 2:
                imagine.blit(brick, (j * Utils.COLUMN_SIZE, i * Utils.ROW_SIZE))
    return imagine


def waitForInput():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return
        pygame.time.wait(1)


def displayDrone(map, path, battery):
    screen = initPygame((map.m * Utils.COLUMN_SIZE, map.n * Utils.ROW_SIZE))
    waitForInput()

    moveDrone(screen, map, path, battery)
    closePygame()

