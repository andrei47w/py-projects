import random as rand
import statistics

from repository import *


class Controller:
    def __init__(self, repo):
        self.__map = repo.getMap()
        self.__mapSurface = self.__map.getMapSurface()
        self.__drone = [5, 5]
        self.__placeDroneOnEmptyPosition()
        self.__repo = repo

    def __placeDroneOnEmptyPosition(self):
        crtX, crtY = self.__drone[0], self.__drone[1]
        while 0 <= crtX < self.__map.getN() and 0 <= crtY < self.__map.getM() and self.__mapSurface[crtX][crtY] == 1:
            crtX, crtY = rand.randint(0, Utils.MAP_SIZE), rand.randint(0, Utils.MAP_SIZE)
        self.__drone[0] = crtX
        self.__drone[1] = crtY

    def iteration(self, populationSize, mutationProbability, crossoverProbability):
        new_population = []
        for _ in range(populationSize):
            parent1 = self.__repo.population.selection()
            parent2 = self.__repo.population.selection()
            newIndividual = Individual(self.__repo.getMap(), Utils.BATTERY)
            offspring, _ = newIndividual.crossover(map=self.__repo.getMap(), firstParent=parent1, secondParent=parent2,
                                                   crossoverProbability=crossoverProbability)
            offspring.mutate(mutationProbability)
            new_population.append(offspring)
        self.__repo.set_new_population(new_population)

    def run(self, populationSize, runs, mutationProbability, crossoverProbability):
        fitness_list_avg = []
        fitness_list_max = []
        best_solution = None
        for _ in range(runs):
            self.iteration(populationSize, mutationProbability, crossoverProbability)
            fitness_list_avg.append(
                statistics.mean([individual.fitness for individual in self.__repo.population.getPopulation()])
            )
            fitness_list_max.append(
                max([individual.fitness for individual in self.__repo.population.getPopulation()])
            )
            for individual in self.__repo.population.getPopulation():
                if best_solution is None or best_solution.fitness < individual.fitness:
                    best_solution = deepcopy(individual)
        path = best_solution.path_of_chromosome()
        return path, fitness_list_avg, fitness_list_max, best_solution.fitness

    def start(self, populationSize, individualSize, runs, battery, mutationProbability, crossoverProbability):
        self.__repo.createPopulation(battery, populationSize, individualSize)

        return self.run(populationSize, runs, mutationProbability, crossoverProbability)

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneX(self):
        return self.__drone[0]

    def getDroneY(self):
        return self.__drone[1]
