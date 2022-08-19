import pickle
from queue import Queue
from random import *

import numpy as np

from utils import *


class Map():
    def __init__(self):
        self.n = Utils.COLUMNS
        self.m = Utils.ROWS
        self.x = int(self.n / 2)
        self.y = int(self.m / 2)
        self.surface = np.zeros((self.n, self.m))
        self.battery = Utils.battery

        self.sensor_index = [[None for _ in range(self.m)] for _ in range(self.n)]
        self.sensor_nr = 0
        self.list_of_sensors = []
        self.sensor_paths = []
        self.first_sensor = None

    def setRandomSensors(self, nr=randint(3, 9)):
        while nr > 0:
            temp_x, temp_y = randint(0, self.n - 1), randint(0, self.n - 1)
            if self.surface[temp_x][temp_y] == 0:
                self.surface[temp_x][temp_y] = 1
                nr -= 1

    def setSensorPaths(self):
        self.surface[self.x][self.y] = 1

        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    self.sensor_index[i][j] = self.sensor_nr
                    self.list_of_sensors.append((i, j))
                    if i == self.x and j == self.y:
                        self.first_sensor = self.sensor_nr
                    self.sensor_nr += 1
        self.sensor_paths = [[None for _ in range(self.sensor_nr)] for _ in
                             range(self.sensor_nr)]

        for sensor in range(self.sensor_nr):
            q = Queue()
            d = [[None for _ in range(self.m)] for _ in range(self.n)]
            prev = [[None for _ in range(self.m)] for _ in range(self.n)]
            sensor_pos = self.list_of_sensors[sensor]
            d[sensor_pos[0]][sensor_pos[1]] = 0
            q.put(sensor_pos)

            while not q.empty():
                current_sensor = q.get()
                for direction in Utils.DIRECTIONS:
                    next_pos = (current_sensor[0] + direction[0], current_sensor[1] + direction[1])
                    if 0 <= next_pos[0] < self.n and 0 <= next_pos[1] < self.m and self.surface[next_pos[0]][
                        next_pos[1]] != 2:
                        if d[next_pos[0]][next_pos[1]] is None:
                            d[next_pos[0]][next_pos[1]] = d[current_sensor[0]][current_sensor[1]] + 1
                            q.put(next_pos)
                            prev[next_pos[0]][next_pos[1]] = current_sensor

            for i in range(self.n):
                for j in range(self.m):
                    if self.surface[i][j] == 1 and (i != sensor_pos[0] or j != sensor_pos[1]) and d[i][j] is not None:
                        current_path = []
                        current_cell = (i, j)

                        while current_cell != sensor_pos:
                            current_path.append(current_cell)
                            current_cell = prev[current_cell[0]][current_cell[1]]
                        self.sensor_paths[sensor][self.sensor_index[i][j]] = list(reversed(current_path))

    def getN(self):
        return self.n

    def getM(self):
        return self.m

    def randomMap(self, fill=0.15):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 2

        self.setRandomSensors()
        self.setSensorPaths()

        with open("random.map", 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def saveMap(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, file_name):
        with open(file_name, "rb") as f:
            new_map = pickle.load(f)
            self.n = new_map.n
            self.m = new_map.m
            self.surface = new_map.surface
            f.close()

    def getMapSurface(self):
        return self.surface

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j])) + " "
            string = string + "\n"
        return string


class Ant:
    def __init__(self, map: Map):
        self.map = map
        self.path = [(map.x, map.y, 0)]
        self.sensor_path = [(self.map.first_sensor, 0)]
        self.battery_left = map.battery
        self.viz = [False for _ in range(self.map.sensor_nr)]
        self.viz[self.map.first_sensor] = True

    def coverage(self):
        marked = [[0 for _ in range(self.map.m)] for _ in range(self.map.n)]
        last_cell = None
        for cell in self.path:
            if cell[2] != 0:
                for direction in Utils.DIRECTIONS:
                    i = cell[0]
                    j = cell[1]
                    for _ in range(cell[2]):
                        new_neighbour = (i + direction[0], j + direction[1])
                        is_wall = True
                        if 0 <= new_neighbour[0] < self.map.n and 0 <= new_neighbour[1] < self.map.m:
                            if self.map.surface[new_neighbour[0]][new_neighbour[1]] != 2:
                                marked[new_neighbour[0]][new_neighbour[1]] = 1
                                i = new_neighbour[0]
                                j = new_neighbour[1]
                                is_wall = False
                        if is_wall:
                            break

        return sum([sum(row) for row in marked])

    def deplete_battery(self):
        temp_cell = self.path.pop()
        self.path.append((temp_cell[0], temp_cell[1], temp_cell[2] + self.battery_left))
        self.battery_left = 0

    def next_path(self, pheromone_matrix, transition_probability):
        current_sensor = self.sensor_path[-1][0]
        possible_next_cells = []

        for sensor in range(self.map.sensor_nr):
            if not self.viz[sensor] and self.map.sensor_paths[current_sensor][sensor] is not None:
                for spend_energy in range(1, int(Utils.ROWS/2) + 1):
                    sensor_distance = len(self.map.sensor_paths[current_sensor][sensor])

                    if self.battery_left < sensor_distance + spend_energy:
                        continue
                    # next_cell = [(sensor, spend_energy), (1 / (spend_energy + sensor_distances)) ** Utils.beta *
                    next_cell = [(sensor, spend_energy), (1 / (sensor_distance)) ** Utils.beta *
                                 pheromone_matrix[current_sensor][sensor][spend_energy] ** Utils.alpha]

                    possible_next_cells.append(next_cell)
        if len(possible_next_cells) == 0:
            return

        if random() < transition_probability:
            next_sensor = None
            max_ph = 0
            for cell in possible_next_cells:
                if next_sensor is None or max_ph < cell[1]:
                    next_sensor = cell[0]
        else:
            next_cell = randint(0, len(possible_next_cells) - 1)
            next_sensor = possible_next_cells[next_cell][0]

        for cell in self.map.sensor_paths[current_sensor][next_sensor[0]]:
            self.path.append((cell[0], cell[1], 0))
            self.battery_left -= 1

        self.path[-1] = (self.path[-1][0], self.path[-1][1], next_sensor[1])
        self.battery_left -= self.path[-1][2]

        self.viz[next_sensor[0]] = True
        self.sensor_path.append(next_sensor)

