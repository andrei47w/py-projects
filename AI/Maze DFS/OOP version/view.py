from random import randint

import numpy as np
import pygame
from pygame.locals import *

from controller import Environment, Drone
from settings import *


class DMap():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def markDetectedWalls(self, e, x, y):
        # mark on this map the walls that you detect
        wals = e.readUDMSensors(x, y)
        i = x - 1
        if wals[UP] > 0:
            while ((i >= 0) and (i >= x - wals[UP])):
                self.surface[i][y] = 0
                i = i - 1
        if (i >= 0):
            self.surface[i][y] = 1

        i = x + 1
        if wals[DOWN] > 0:
            while ((i < self.__n) and (i <= x + wals[DOWN])):
                self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1

        j = y + 1
        if wals[LEFT] > 0:
            while ((j < self.__m) and (j <= y + wals[LEFT])):
                self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1

        j = y - 1
        if wals[RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[RIGHT])):
                self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1

        return None

    def image(self, x, y):

        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)

        for i in range(self.__n):
            for j in range(self.__m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                elif (self.surface[i][j] == 0):
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("extra files\\drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine


class View:
    def __init__(self):
        # we create the environment
        self.e = Environment()
        self.e.loadEnvironment("extra files\\test2.map")
        # print(str(e))

        # we create the map
        self.m = DMap()

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("extra files\\logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)

        # cream drona
        self.d = Drone(x, y)

        # create a surface on screen that has the size of 800 x 480
        self.screen = pygame.display.set_mode((800, 400))
        self.screen.fill(WHITE)
        self.screen.blit(self.e.image(), (0, 0))

    def start(self):
        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                if event.type == KEYDOWN:
                    # use this function instead of move
                    # d.moveDSF(m)
                    self.d.move(self.m)
            self.m.markDetectedWalls(self.e, self.d.x, self.d.y)
            self.screen.blit(self.m.image(self.d.x, self.d.y), (400, 0))
            pygame.display.flip()

        pygame.quit()
