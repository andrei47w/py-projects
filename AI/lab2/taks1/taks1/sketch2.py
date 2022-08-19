# import the pygame module, so you can use it
import copy
import pickle
import time
from math import sqrt
from random import random, randint

import numpy as np
import pygame
from pygame.locals import *

# Creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class BonusSearch():
    def __init__(self):
        self.dirs = [
            lambda x, y, z, p: (x, y - 1, z + 1, p + [(x, y)]),
            lambda x, y, z, p: (x, y + 1, z + 1, p + [(x, y)]),
            lambda x, y, z, p: (x - 1, y, z + 1, p + [(x, y)]),
            lambda x, y, z, p: (x + 1, y, z + 1, p + [(x, y)]),
        ]

    def valid(self, grid, x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

    def adjacent(self, grid, frontier):
        for (x, y, z, p) in frontier:
            for d in self.dirs:
                nx, ny, nz, np = d(x, y, z, p)
                if self.valid(grid, nx, ny):
                    yield (nx, ny, nz, np)

    def flood(self, grid, frontier):
        res = list(self.adjacent(grid, frontier))
        for (x, y, z, p) in frontier:
            grid[x][y] = 1
        return res

    def shortest(self, m, start, end):
        grid = copy.deepcopy(m.surface)

        start, end = tuple(start), tuple(end)
        frontier = [(start[0], start[1], 0, [])]
        res = []
        while frontier and grid[end[0]][end[1]] == 0:
            frontier = self.flood(grid, frontier)
            for (x, y, z, p) in frontier:
                if (x, y) == end:
                    res.append((z, p + [(x, y)]))
        if not res:
            return ()

        return sorted(res)[0]


class Map():
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))

        return mapImage


def make_steps_Greedy(x, y, finalX, finalY, temp_m, count):
    count += 1
    temp_m[x][y] = count
    if x == finalX and y == finalY:
        return temp_m

    if x > 0:
        if 0 == temp_m[x - 1][y]:
            make_steps_Greedy(x - 1, y, finalX, finalY, temp_m, count)
    if x < 19:
        if 0 == temp_m[x + 1][y]:
            make_steps_Greedy(x + 1, y, finalX, finalY, temp_m, count)
    if y > 0:
        if 0 == temp_m[x][y - 1]:
            make_steps_Greedy(x, y - 1, finalX, finalY, temp_m, count)
    if y < 19:
        if 0 == temp_m[x][y + 1]:
            make_steps_Greedy(x, y + 1, finalX, finalY, temp_m, count)


def make_step_A(k, temp_m):
    for i in range(len(temp_m)):
        for j in range(len(temp_m[i])):
            if temp_m[i][j] == k:
                if i > 0 and temp_m[i - 1][j] == 0:
                    temp_m[i - 1][j] = k + 1
                if j > 0 and temp_m[i][j - 1] == 0:
                    temp_m[i][j - 1] = k + 1
                if i < len(temp_m) - 1 and temp_m[i + 1][j] == 0:
                    temp_m[i + 1][j] = k + 1
                if j < len(temp_m[i]) - 1 and temp_m[i][j + 1] == 0:
                    temp_m[i][j + 1] = k + 1



def searchGreedy(mapM, initialX, initialY, finalX, finalY):
    m = mapM.surface

    temp_m = [[0 for i in range(len(m))] for j in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] == 1:
                temp_m[i][j] = -1

    make_steps_Greedy(initialX, initialY, finalX, finalY, temp_m, 0)

    i, j = finalX, finalY
    k = temp_m[i][j]
    path = [(i, j)]
    while k > 1:
        if i > 0 and temp_m[i - 1][j] == k - 1:
            i, j = i - 1, j
            path.append((i, j))
            k -= 1
        elif j > 0 and temp_m[i][j - 1] == k - 1:
            i, j = i, j - 1
            path.append((i, j))
            k -= 1
        elif i < len(temp_m) - 1 and temp_m[i + 1][j] == k - 1:
            i, j = i + 1, j
            path.append((i, j))
            k -= 1
        elif j < len(temp_m[i]) - 1 and temp_m[i][j + 1] == k - 1:
            i, j = i, j + 1
            path.append((i, j))
            k -= 1

    return path


def searchAStar(mapM, initialX, initialY, finalX, finalY):
    m = mapM.surface

    temp_m = [[0 for i in range(len(m))] for j in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] == 1:
                temp_m[i][j] = -1
            if i == initialX and j == initialY:
                temp_m[i][j] = 1

    k = 0
    while temp_m[finalX][finalY] == 0:
        k += 1
        make_step_A(k, temp_m)

    i, j = finalX, finalY
    k = temp_m[i][j]
    path = [(i, j)]
    while k > 1:
        if i > 0 and temp_m[i - 1][j] == k - 1:
            i, j = i - 1, j
            path.append((i, j))
            k -= 1
        elif j > 0 and temp_m[i][j - 1] == k - 1:
            i, j = i, j - 1
            path.append((i, j))
            k -= 1
        elif i < len(temp_m) - 1 and temp_m[i + 1][j] == k - 1:
            i, j = i + 1, j
            path.append((i, j))
            k -= 1
        elif j < len(temp_m[i]) - 1 and temp_m[i][j + 1] == k - 1:
            i, j = i, j + 1
            path.append((i, j))
            k -= 1

    return path


def dummysearch():
    # example of some path in test1.map from [5,7] to [7,11]
    return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]


def displayWithPath(image, path, color):
    mark = pygame.Surface((20, 20))
    mark.fill(color)
    for move in path:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image


# define a main function
def main():
    # we create the map
    m = Map()
    # m.randomMap()
    # m.saveMap("test2.map")
    m.loadMap("test1.map")

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # create drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400, 400))
    screen.fill(WHITE)

    # define a variable to control the main loop
    running = True

    # final position
    final_x = 2
    final_y = 3

    # main loop
    path_A = path_G = path_B = []
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_1]:
                    startTime = time.time()

                    path_A = searchAStar(m, d.x, d.y, final_x, final_y)
                    print('\n   A*\n', path_A, '\nexecution time:', time.time() - startTime, '\nlength:', len(path_A))

                if pressed_keys[K_2]:
                    startTime = time.time()
                    path_G = searchGreedy(m, d.x, d.y, final_x, final_y)
                    print('\n   Greedy\n', path_G, '\nexecution time:', time.time() - startTime, '\nlength:', len(path_G))

                if pressed_keys[K_3]:
                    bonusSearch = BonusSearch()
                    startTime = time.time()
                    result = bonusSearch.shortest(m, (d.x, d.y), (final_x, final_y))[1]
                    endTime = time.time()
                    path_B = [ele for ele in reversed(result)]
                    print('\n   Uniform Cost Search\n', path_B, '\nexecution time:', endTime - startTime, '\nlength:', len(path_B))


        screen.blit(d.mapWithDrone(m.image()), (0, 0))

        pygame.display.flip()

    if path_G:
        screen.blit(displayWithPath(m.image(), path_G, GRAYBLUE), (0, 0))
        pygame.display.flip()
        if path_A or path_B:
            time.sleep(5)
    if path_A:
        screen.blit(displayWithPath(m.image(), path_A, GREEN), (0, 0))
        pygame.display.flip()
        if path_B:
            time.sleep(5)
    if path_B:
        screen.blit(displayWithPath(m.image(), path_B, YELLOW), (0, 0))
        pygame.display.flip()
    # path = dummysearch()
    # screen.blit(displayWithPath(m.image(), path), (0, 0))

    pygame.display.flip()
    time.sleep(5)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
