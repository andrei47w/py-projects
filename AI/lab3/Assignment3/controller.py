import random as rand
import statistics

from repository import *


class Controller:
    def __init__(self, repo):
        self.__map = repo.getMap()
        self.__mapSurface = self.__map.getMapSurface()
        self.fixDronePos()
        self.__repo = repo
        self.__population = None

        self.fitness_list_avg = None
        self.fitness_list_max = None

    def fixDronePos(self):
        crtX, crtY = self.__map.x, self.__map.y

        while 0 <= crtX < self.__map.getN() and 0 <= crtY < self.__map.getM() and self.__mapSurface[crtX][crtY] == 1:
            crtX, crtY = rand.randint(0, Utils.MAP_SIZE), rand.randint(0, Utils.MAP_SIZE)

        self.__map.x, self.__map.y = crtX, crtY

    def iteration(self, populationSize, mutationProbability, crossoverProbability):
        new_population = []

        for _ in range(populationSize):
            firstParent, secondParent = self.__population.selection(), self.__population.selection()
            child = Individual(self.__repo.getMap(), Utils.BATTERY).\
                crossover(map=self.__repo.getMap(), firstParent=firstParent, secondParent=secondParent, crossoverProbability=crossoverProbability)

            child.mutate(mutationProbability)
            new_population.append(child)

        self.__population = Population(self.__repo.getMap(), Utils.BATTERY, populationSize, Utils.POPULATION_SIZE, population=new_population)

    def run(self, populationSize, individualSize, runs, battery, mutationProbability, crossoverProbability):
        # (Utils.POPULATION_SIZE,
        #  Utils.INDIVIDUAL_SIZE,
        #  Utils.RUNS,
        #  Utils.BATTERY,
        #  Utils.MUTATION_PROBABILITY,
        #  Utils.CROSSOVER_PROBABILITY)

        self.__population = Population(self.__map, battery, populationSize, individualSize)

        self.fitness_list_avg = []
        self.fitness_list_max = []
        best_individual = None

        for _ in range(runs):
            self.iteration(populationSize, mutationProbability, crossoverProbability)

            fitness_list = []
            for individual in self.__population.getPopulation():
                fitness_list.append(individual.fitness)

            self.fitness_list_avg.append(statistics.mean(fitness_list))
            self.fitness_list_max.append(max(fitness_list))

            for individual in self.__population.getPopulation():
                if best_individual is None or best_individual.fitness < individual.fitness:
                    best_individual = deepcopy(individual)

        return best_individual

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneX(self):
        return self.__map.x

    def getDroneY(self):
        return self.__map.y
