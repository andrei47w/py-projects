import time

from domain import Map
from utils import *
from controller import Controller
from gui import displayDrone


def run():
    print('\n\n\t\tMenu\n'
          '1. map options:\n'
          '\ta. create random map\n'
          '\tb. load a map\n'
          '\tc. save a map')
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
        else:
            print('invalid input')

    start_time = time.time()
    controller = Controller(map)
    solver = controller.run()
    end_time = time.time()

    print("Scanned " + str(solver.coverage()) + " cells")
    print("Path: " + str(solver.path))
    print("Execution time: " + str(end_time - start_time))

    displayDrone(controller.map, solver.path, Utils.battery)


if __name__ == '__main__':
    run()
