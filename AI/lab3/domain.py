# -*- coding: utf-8 -*-
import pickle
from copy import deepcopy
from random import *
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
            self.x = [gene().random() for _ in range(self.size)]  # chromosome
        else:
            self.x = x

    def fitness(self):
        path = self.createPath()
        count = 0

        for pos in path:
            # print(pos[0])
            count += 1

            for i in Utils.DIRECTIONS:
                temp_pos = deepcopy(pos)
                ok = True

                while ok:
                    temp_pos[0] += i[0]
                    temp_pos[1] += i[1]
                    ok = False
                    if 0 <= temp_pos[0] < self.map.getN() and 0 <= temp_pos[1] < self.map.getM() \
                            and self.map.getMapSurface()[temp_pos[0]][temp_pos[1]] != 1:
                        ok = True
                        count += 1

        #  BONUS
        if Utils.BONUS and path[0] == path[-1]:
            count **= 2

        self.fitness = count

    def createPath(self):
        drone = [self.map.x, self.map.y]
        path = []

        path.append(drone)
        for i in range(len(self.x)):
            new_drone = [drone[0] + Utils.DIRECTIONS[self.x[i]][0], drone[1] + Utils.DIRECTIONS[self.x[i]][1]]
            if 0 <= new_drone[0] < self.map.getN() and 0 <= new_drone[1] < self.map.getM() \
                    and self.map.getMapSurface()[new_drone[0]][new_drone[1]] != 1 and self.battery >= len(path):
                drone = new_drone
                path.append(drone)
            else:
                break

        return path

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            i = randrange(len(self.x))
            j = randrange(len(self.x))
            self.x[i], self.x[j] = self.x[j], self.x[i]

    @staticmethod
    def crossover(map, firstParent, secondParent, crossoverProbability=0.8):
        size = len(firstParent.x)

        if random() < crossoverProbability:
            crossover_point = randint(0, size)

            new_x = []
            for i in range(size):
                if i > crossover_point:
                    new_x.append(firstParent.x[i])
                else:
                    new_x.append(secondParent.x[i])

            return Individual(map, firstParent.battery, x=new_x)
        else:
            return Individual(map, firstParent.battery, size)


class Population():
    def __init__(self, map, battery=5, populationSize=25, individualSize=25, population=None):
        self.__populationSize = populationSize
        self.__map = map
        self.__battery = battery
        self.__individualSize = individualSize
        if population is not None:
            self.__population = population
        else:
            self.__population = self.getNewPopulation()

        self.evaluate()

    def getNewPopulation(self):
        population = []
        for i in range(self.__populationSize):
            population.append(Individual(self.__map, self.__battery, self.__individualSize))

        return population

    def evaluate(self):
        for x in self.__population:
            x.fitness()

    def selection(self, k=Utils.SAMPLE_SIZE):
        # perform a selection of k individuals from the population
        # and returns that selection
        new_sample = sample(self.__population, k)
        best_individual = new_sample[0]
        for individual in new_sample:
            if best_individual.fitness < individual.fitness:
                best_individual = individual

        return best_individual

    def getPopulation(self):
        return self.__population


class Map():
    def __init__(self):
        self.__n = Utils.MAP_SIZE
        self.__m = Utils.MAP_SIZE
        self.x = int(self.__n / 2)
        self.y = int(self.__m / 2)
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
