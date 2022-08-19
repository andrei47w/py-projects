# -*- coding: utf-8 -*-
import math
import time

from PIL import Image
from matplotlib import pyplot

from controller import *
from gui import *
from repository import *


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class UI():
    def __init__(self):
        pass

    @staticmethod
    def __setup_param():
        Utils.MAP_SIZE = int(input('MAP_SIZE='))
        Utils.ANIMATION_TIME = int(input('ANIMATION_TIME='))
        Utils.RUNS = int(input('RUNS='))
        Utils.POPULATION_SIZE = int(input('POPULATION_SIZE='))
        Utils.SAMPLE_SIZE = int(input('SAMPLE_SIZE='))
        Utils.CROSSOVER_PROBABILITY = int(input('CROSSOVER_PROBABILITY='))
        Utils.INDIVIDUAL_SIZE = int(input('INDIVIDUAL_SIZE='))
        Utils.MUTATION_PROBABILITY = int(input('MUTATION_PROBABILITY='))
        Utils.BATTERY = int(input('BATTERY='))
        Utils.BONUS = bool(input('BONUS='))

    def run(self):
        print('\n\n\t\tMenu\n'
              '1. map options:\n'
              '\ta. create random map\n'
              '\tb. load a map\n'
              '\tc. save a map\n'
              '\td. visualise map')
        map = Map()

        while True:
            option1 = input('option: ')
            if option1 == 'a':
                map.randomMap()
                break
            elif option1 == 'b':
                file_name = input('file name: ')
                map.loadMap('extra/' + file_name)
                break
            elif option1 == 'c':
                map.randomMap()
                file_name = input('file name: ')
                map.saveMap('extra/' + file_name)
                break
            elif option1 == 'd':
                file_name = input('file name: ')
                map.loadMap('extra/' + file_name)

                repo = repository(map)
                controller = Controller(repo)
                gui = GUI(controller)
                gui.visualizeMap()
                break
            else:
                print('invalid input')

        print('\n2. EA options:\n'
              '\ta. parameters setup\n'
              '\tb. run the solver\n'
              '\tc. visualise the statistics\n'
              '\td. view the drone moving on a path')

        repo, controller, path = None, None, []
        while True:
            option2 = input('option: ')

            if option2 == 'a':
                self.__setup_param()

            elif option2 == 'b':
                repo = repository(map)
                controller = Controller(repo)

                startTime = time.time()
                individual = controller.run(Utils.POPULATION_SIZE,
                                            Utils.INDIVIDUAL_SIZE,
                                            Utils.RUNS,
                                            Utils.BATTERY,
                                            Utils.MUTATION_PROBABILITY,
                                            Utils.CROSSOVER_PROBABILITY)
                endTime = time.time()
                print("execution time:", endTime - startTime,
                      '\ncells discovered:', math.sqrt(individual.fitness))
                path = individual.createPath()

            elif option2 == 'c':
                print('\ta. fitness\n'
                      '\tb. standard deviation')
                option3 = input('option: ')

                if option3 == 'a':
                    repo = repository(map)
                    controller = Controller(repo)

                    startTime = time.time()
                    individual = controller.run(Utils.POPULATION_SIZE,
                                                Utils.INDIVIDUAL_SIZE,
                                                Utils.RUNS,
                                                Utils.BATTERY,
                                                Utils.MUTATION_PROBABILITY,
                                                Utils.CROSSOVER_PROBABILITY)
                    endTime = time.time()
                    print("execution time:", endTime - startTime,
                          '\ncells discovered:', math.sqrt(individual.fitness))

                    pyplot.plot(controller.fitness_list_avg)
                    pyplot.plot(controller.fitness_list_max)
                    pyplot.savefig("output/fitness.png")
                    pyplot.close()

                    image = Image.open('output/fitness.png')
                    image.show()
                elif option3 == 'b':
                    repo = repository(map)
                    controller = Controller(repo)

                    values = []
                    for i in range(30):
                        seed(i)
                        individual = controller.run(Utils.POPULATION_SIZE,
                                                    Utils.INDIVIDUAL_SIZE,
                                                    Utils.RUNS,
                                                    Utils.BATTERY,
                                                    Utils.MUTATION_PROBABILITY,
                                                    Utils.CROSSOVER_PROBABILITY)
                        values.append(individual.fitness)
                    avg = statistics.mean(values)
                    stdev = statistics.stdev(values)
                    print("avg solution fitness:", avg, "\nstdev:", stdev)
                    pyplot.plot(values)
                    pyplot.ylim([0, None])
                    pyplot.savefig("output/stdev.png")
                    pyplot.close()

                    image = Image.open('output/stdev.png')
                    image.show()
                else:
                    print('invalid input')

            elif option2 == 'd':
                if controller:
                    gui = GUI(controller)
                    gui.start(path)
                else:
                    print('No path generated')
            else:
                print('invalid input')


if __name__ == '__main__':
    ui = UI()
    ui.run()
