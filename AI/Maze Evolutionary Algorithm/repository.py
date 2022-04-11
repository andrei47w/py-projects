# -*- coding: utf-8 -*-

from domain import *


class repository():
    def __init__(self, Map):
        self.__population = []
        self.__map = Map

    def getMap(self):
        return self.__map

    def createPopulation(self, battery, populationSize, individualSize):
        self.population = Population(self.__map, battery, populationSize, individualSize)

    def set_new_population(self, population_list):
        self.population = Population(self.__map, population=population_list)

    def getPopulation(self):
        return self.__population
