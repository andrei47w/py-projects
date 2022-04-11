# -*- coding: utf-8 -*-

class Utils():
    # Creating some colors
    BLUE = (0, 0, 255)
    GRAYBLUE = (50, 120, 120)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # define directions
    UP = 0
    DOWN = 2
    LEFT = 1
    RIGHT = 3

    # define indexes variations
    DIRECTIONS = [[-1, 0], [1, 0], [0, 1], [0, -1]]

    # define mapsize

    MAP_SIZE = 20

    ANIMATION_TIME = 250

    POPULATION_SIZE = 50
    GENERATION_COUNT = 25
    INDIVIDUAL_SIZE = 20
    RUNS = 25
    BATTERY = 10
    MUTATION_PROBABILITY = 0.04
    CROSSOVER_PROBABILITY = 0.8
