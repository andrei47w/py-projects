from copy import deepcopy

from domain import Map, Ant
from utils import *


class Controller:
    def __init__(self, map: Map):
        self.ants = Utils.ants
        self.degradation_coeff = Utils.degradation_coeff
        self.transition_probability = Utils.transition_probability
        self.map = map
        self.pheromone_matrix = self.init_pheromone_matrix()
        # print(*self.pheromone_matrix, sep='\n')
        self.initial_pheromone_matrix = deepcopy(self.pheromone_matrix)

    def init_pheromone_matrix(self):
        temp = []
        for i in range(self.map.sensor_nr):
            temp.append([])
            for j in range(self.map.sensor_nr):
                if i != j:
                    temp[-1].append([1] * (int(Utils.ROWS/2) + 1))
                else:
                    temp[-1].append([0] * (int(Utils.ROWS/2) + 1))

        return temp

    def iterate(self):
        ant_list = [Ant(self.map) for _ in range(self.ants)]

        for _ in range(self.map.battery):
            for ant in ant_list:
                ant.next_path(self.pheromone_matrix, self.transition_probability)
        for ant in ant_list:
            ant.deplete_battery()

        for i in range(self.map.sensor_nr):
            for j in range(self.map.sensor_nr):
                for spent_energy in range(int(Utils.ROWS/2) + 1):
                    self.pheromone_matrix[i][j][spent_energy] = (1 - self.degradation_coeff) * self.pheromone_matrix[i][j][
                        spent_energy] + self.degradation_coeff * self.initial_pheromone_matrix[i][j][spent_energy]

        for ant in ant_list:
            for i in range(len(ant.sensor_path) - 1):
                x = ant.sensor_path[i]
                y = ant.sensor_path[i + 1]
                self.pheromone_matrix[x[0]][y[0]][y[1]] += 1 / (len(ant.sensor_path) - 1)

        max_coverage = 0
        best_ant = ant_list[0]
        for ant in ant_list:
            if max_coverage < ant.coverage():
                max_coverage = ant.coverage()
                best_ant = ant

        return best_ant

    def run(self):
        solver = None
        for _ in range(Utils.iterations):
            current_solution = self.iterate()

            if solver is None or solver.coverage() < current_solution.coverage():
                solver = current_solution

        return solver
