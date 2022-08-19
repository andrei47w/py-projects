# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from domain import *


class GUI:
    def __init__(self, controller):
        pygame.init()
        logo = pygame.image.load("extra/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")
        self.__screen = pygame.display.set_mode((400, 400))
        self.__screen.fill(Utils.WHITE)
        self.__controller = controller

    def getMapSurface(self):
        return self.__controller.getMapSurface()

    def __image(self, colour=Utils.BLUE, background=Utils.WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)

        mapSurface = self.__controller.getMapSurface()
        for i in range(Utils.MAP_SIZE):
            for j in range(Utils.MAP_SIZE):
                if mapSurface[i][j] == 1:
                    image.blit(brick, (j * 20, i * 20))

        return image

    def __closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()

    def __moveDroneAlongPath(self, droneImage, pathImage, codedPath):
        pathTile = pygame.Surface((20, 20))
        pathTile.fill(Utils.GREEN)

        crtPosition = (self.__controller.getDroneX(), self.__controller.getDroneY())

        for directionCode in codedPath:
            pathImage.blit(pathTile, (crtPosition[1] * 20, crtPosition[0] * 20))
            pathImageCopy = pathImage.copy()
            pathImageCopy.blit(droneImage, (crtPosition[1] * 20, crtPosition[0] * 20))
            self.__screen.blit(pathImageCopy, (0, 0))
            pygame.display.update()
            pygame.time.wait(Utils.ANIMATION_TIME)

            direction = Utils.DIRECTIONS[directionCode]
            crtPosition = (crtPosition[0] + direction[0], crtPosition[1] + direction[1])

    def __movingDrone(self, droneImage, path, markSeen=True):
        # animation of a drone on a path
        for i in range(len(path)):
            self.__screen.blit(self.__image(), (0, 0))

            if markSeen:
                brick = pygame.Surface((20, 20))
                brick.fill(Utils.GREEN)
                for j in range(i + 1):
                    for var in Utils.DIRECTIONS:
                        x = path[j][0]
                        y = path[j][1]
                        while ((0 <= x + var[0] < Utils.MAP_SIZE and
                                0 <= y + var[1] < Utils.MAP_SIZE) and
                               self.getMapSurface()[x + var[0]][y + var[1]] != 1):
                            x = x + var[0]
                            y = y + var[1]
                            self.__screen.blit(brick, (y * 20, x * 20))

            self.__screen.blit(droneImage, (path[i][1] * 20, path[i][0] * 20))
            pygame.display.flip()
            pygame.time.wait(Utils.ANIMATION_TIME)

    def __displayMap(self):
        droneImage = pygame.image.load("extra/drona.png")
        pathImage = self.__image()
        pathImage.blit(droneImage, (self.__controller.getDroneY() * 20, self.__controller.getDroneX() * 20))
        self.__screen.blit(pathImage, (0, 0))
        pygame.display.update()
        return droneImage, pathImage

    def displayWithPath(self, path):
        droneImage, pathImage = self.__displayMap()
        # then progressively show the actual path of the drone
        self.__movingDrone(droneImage, path)
        # self.__moveDroneAlongPath(droneImage, pathImage, codedPath)
        self.waitForInput()

    def waitForInput(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            pygame.time.wait(1)

    def start(self, path):
        self.__displayMap()
        self.waitForInput()

        self.displayWithPath(path)
        self.__closePyGame()

    def visualizeMap(self):
        self.__displayMap()
        self.waitForInput()

        self.__closePyGame()
