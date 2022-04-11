# -*- coding: utf-8 -*-
import pickle
from random import *
from copy import deepcopy
import numpy as np

from extra.utils import *


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

class gene:
    def __init__(self):
        # random initialise the gene according to the representation
        self.__number = randrange(0, 4)

    def random(self):
        return self.__number


class Individual:
    def __init__(self, map, battery, size=0, x=None):
        self.battery = battery
        self.map = map
        self.size = size
        if not x:
            self.x = [gene().random() for i in range(self.size)]  # chromosome
        else:
            self.x = x
        self.f = None  # fitness

    def fitness(self):
        path = self.path_of_chromosome()
        marked = [[0 for _ in range(self.map.getM())] for _ in range(self.map.getN())]
        for position in path:
            # print(position[0])
            marked[position[0]][position[1]] = 1
            for direction in Utils.DIRECTIONS:
                sight = deepcopy(position)
                while True:
                    sight[0] += direction[0]
                    sight[1] += direction[1]
                    valid = False
                    if 0 <= sight[0] < self.map.getN() and 0 <= sight[1] < self.map.getM():
                        if self.map.getMapSurface()[sight[0]][sight[1]] != 1:
                            valid = True
                    if not valid:
                        break
                    marked[sight[0]][sight[1]] = 1
        self.fitness = sum([sum(row) for row in marked])

    def path_of_chromosome(self):
        drone = [self.map.x, self.map.y]
        path = []

        path.append(drone)
        for i in range(len(self.x)):
            new_drone = [drone[0] + Utils.DIRECTIONS[self.x[i]][0], drone[1] + Utils.DIRECTIONS[self.x[i]][1]]
            if 0 <= new_drone[0] < self.map.getN() and 0 <= new_drone[1] < self.map.getM():
                if self.map.getMapSurface()[new_drone[0]][new_drone[1]] != 1:
                    if self.battery >= len(path):
                        drone = new_drone
                        path.append(drone)

        return path

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability and len(self.x) >= 2:
            i = 0
            j = 0
            while i == j:
                i = randrange(len(self.x))
                j = randrange(len(self.x))
            self.x[i], self.x[j] = self.x[j], self.x[i]
            # perform a mutation with respect to the representation

    def crossover(self, map, firstParent, secondParent, crossoverProbability=0.8):
        size = len(firstParent.x)

        if random() < crossoverProbability:
            cutting_point = randint(0, size)
            offspring1 = Individual(map, firstParent.battery, x=[
                firstParent.x[i] if i < cutting_point else secondParent.x[i] for i in range(size)])
            offspring2 = Individual(map, firstParent.battery, x=[
                firstParent.x[i] if i < cutting_point else secondParent.x[i] for i in range(size)])
        else:
            offspring1, offspring2 = Individual(map, firstParent.battery, size), Individual(map, firstParent.battery, size)

        return offspring1, offspring2


class Population():
    def __init__(self, map, battery=5, populationSize=25, individualSize=25, population=None):
        self.__populationSize = populationSize
        self.__map = map
        self.__battery = battery
        self.__individualSize = individualSize
        if population:
            self.__population = population
        else:
            self.__population = [Individual(map, battery, individualSize) for _ in range(populationSize)]

        self.evaluate()

    def evaluate(self):
        for x in self.__population:
            x.fitness()

    def selection(self, k=2):
        # perform a selection of k individuals from the population
        # and returns that selection
        return sorted(sample(self.__population, k), key=lambda x: x.fitness, reverse=True)[0]

    def getPopulation(self):
        return self.__population


class Map():
    def __init__(self):
        self.__n = Utils.MAP_SIZE
        self.__m = Utils.MAP_SIZE
        self.x = 5
        self.y = 5
        self.__surface = np.zeros((self.__n, self.__m))

    def getN(self):
        return self.__n

    def getM(self):
        return self.__m

    def randomMap(self, fill=0.15):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = 1

    def saveMap(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, file_name):
        with open(file_name, "rb") as f:
            new_map = pickle.load(f)
            self.__n = new_map.__n
            self.__m = new_map.__m
            self.__surface = new_map.__surface
            f.close()

    def getMapSurface(self):
        return self.__surface

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j])) + " "
            string = string + "\n"
        return string
