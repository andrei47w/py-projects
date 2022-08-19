# import the pygame module, so you can use it
import pickle
from random import random

import numpy as np
import pygame
from pygame.locals import *

from settings import *


class Environment():
    def __init__(self):
        self.__n = N
        self.__m = M
        self.__surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__n) and (self.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__m) and (self.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cols = 20
        self.rows = 20

        self.path_queue = []

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

        if pressed_keys[K_p]:
            self.moveDSF(detectedMap)

    def dfs(self, node, map, path):
        if node not in path:
            path.append(node)

            for neighbour in [(node[0], node[1] - 1), (node[0], node[1] + 1), (node[0] - 1, node[1]),
                              (node[0] + 1, node[1])]:
                if 0 <= neighbour[0] <= 19 and 0 <= neighbour[1] <= 19:
                    if map[neighbour[0], neighbour[1]] == 0:
                        path = self.dfs(neighbour, map, path)

                    # elif map[neighbour[0], neighbour[1]] == -1:
                    #     return path

        return path

    def neighbour_check(self, map, i, j, n_type):
        if j + 1 < self.cols and map[i, j + 1] == n_type:
            return True
        if i + 1 < self.rows and map[i + 1, j] == n_type:
            return True
        if 0 <= i - 1 and map[i - 1, j] == n_type:
            return True
        if 0 <= j - 1 and map[i, j - 1] == n_type:
            return True
        return False

    def moveDSF(self, detectedMap):
        map = detectedMap.surface

        if not self.path_queue:
            path = []
            self.dfs((self.x, self.y), map, path)
            # print(path)

            last_intersection = 0
            new_discovery = False
            for i in range(len(path) - 1):
                if self.neighbour_check(map, path[i][0], path[i][1], -1):
                    new_discovery = True

                if i != 0 and not path[i + 1] in [(path[i][0], path[i][1] - 1), (path[i][0], path[i][1] + 1),
                                                  (path[i][0] - 1, path[i][1]), (path[i][0] + 1, path[i][1])]:
                    if not new_discovery:
                        path = path[:last_intersection - 1] + path[i + 1:]
                    else:
                        last_intersection = i
                        # path = path[:i+1]
                        # break
                        # if 0 <= path[i][0] <= 19 and 0 <= path[i][1] <= 19:
                        j = i
                        temp = path[i + 1]
                        while j > 0:
                            j -= 1
                            path.insert(i + i - j, path[j])
                            # print(path[j], j)
                            if temp in [(path[j][0], path[j][1] - 1), (path[j][0], path[j][1] + 1),
                                        (path[j][0] - 1, path[j][1]), (path[j][0] + 1, path[j][1])]:
                                break

            last_good_node = 1
            for i in range(len(path) - 2):
                if self.neighbour_check(map, path[i][0], path[i][1], -1):
                    last_good_node = i

                if i != 0 and not path[i + 1] in [(path[i][0], path[i][1] - 1), (path[i][0], path[i][1] + 1),
                                                  (path[i][0] - 1, path[i][1]), (path[i][0] + 1, path[i][1])]:
                    path = path[:i]
                    break
            path = path[:last_good_node + 1]

            # print(path)

            # print("cox", self.findShortestPathLength(map, (path[-1][0], path[-1][1]), (self.x, self.y)))

            self.path_queue += path[1:]

        self.x = self.path_queue[0][0]
        self.y = self.path_queue[0][1]

        self.path_queue = self.path_queue[1:]
