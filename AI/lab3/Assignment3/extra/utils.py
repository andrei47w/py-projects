# -*- coding: utf-8 -*-

class Utils():
    # Creating some colors
    BLUE = (0, 0, 255)
    GRAYBLUE = (50, 120, 120)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # define indexes variations
    DIRECTIONS = [[-1, 0], [1, 0], [0, 1], [0, -1]]

    # define mapsize
    MAP_SIZE = 20

    # define animation delay
    ANIMATION_TIME = 250

    # define algorithm parameters
    POPULATION_SIZE = 100
    INDIVIDUAL_SIZE = 20
    SAMPLE_SIZE = 5
    RUNS = 2
    BATTERY = 18
    MUTATION_PROBABILITY = 0.04
    CROSSOVER_PROBABILITY = 0.8

    BONUS = True
