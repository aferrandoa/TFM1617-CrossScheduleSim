"""Ant colony system class"""
import random as rd
import numpy as np

from vo.AntData import AntData

class AntColonySystem(object):
    """Ant colony system"""

    def __init__(self, i_inner_data, i_representation, i_ant_number, i_pherom_ini_value,
                 i_iterations_number, i_q_value, i_b_value, i_p_value, i_a_value):
        self.inner_data = i_inner_data
        self.representation = i_representation
        self.ant_number = i_ant_number
        self.pherom_ini_value = i_pherom_ini_value
        self.pheromone_values = []
        self.ant_status = []
        self.iterations_number = i_iterations_number
        self.q_value = i_q_value
        self.b_value = i_b_value
        self.p_value = i_p_value
        self.a_value = i_a_value
        self.best_solution = None
        self.best_solution_value = float("inf")

    def initialize(self):
        """Initialize the ants and pheromones"""
        nodes_num = len(self.representation.edge_list)
        calculated_pheromone = (nodes_num * self.pherom_ini_value)**-1
        self.pherom_ini_value = calculated_pheromone
        self.pheromone_values = np.ones((nodes_num, nodes_num)) * calculated_pheromone

        self.initialize_ants()

    def initialize_ants(self):
        """Inits/Resets all the ants"""
        for i in range(0, self.ant_number):
            ant_vertex = self.representation.vertex_list[:]
            first_car = ant_vertex[0]
            ant_vertex.remove(first_car)

            current_ant = AntData(i, 0, ant_vertex)
            current_ant.current_solution.append(0)
            self.ant_status.append(current_ant)

    def run(self):
        """Starts the process"""
        for current_iteration in range(0, self.iterations_number):
            for current_ant in self.ant_status:
                self.search_for_solution(current_ant)

            best_ant_id = self.get_best_ant()
            self.best_solution = self.ant_status[best_ant_id].current_solution
            self.best_solution_value = self.ant_status[best_ant_id].current_solution_value
            self.global_pheromone_update(best_ant_id)

            #print 'Best solution in iteration %d' % current_iteration
            #print 'PATH: %s' % self.best_solution
            #print 'LENGTH: %s' % self.best_solution_value

            self.initialize_ants()

        return self.convert_solution(self.best_solution)

    def search_for_solution(self, i_current_ant):
        """Search for a solution for the current ant"""
        while len(i_current_ant.pendindg_dests) > 0:
            possible_dests = self.redux_to_possible(i_current_ant)
            next_node = self.select_next_node(i_current_ant, possible_dests)

            selected_car = self.representation.vertex_list[next_node]
            i_current_ant.current_solution.append(next_node)
            i_current_ant.current_solution_value = self.get_path_value(i_current_ant.current_solution)
            i_current_ant.pendindg_dests.remove(selected_car)
            self.local_pheromone_update(i_current_ant.current_car, next_node)
            i_current_ant.current_car = next_node

    def redux_to_possible(self, i_current_ant):
        """A destiny node can only be reached if there is not an earlier car pending"""
        possible_dests = self.representation.edge_list[i_current_ant.current_car]
        reachable_cars = []

        for current_to_car_id in possible_dests:
            current_to_car = self.representation.vertex_list[current_to_car_id]

            if (current_to_car not in i_current_ant.pendindg_dests
                    or (current_to_car_id == len(self.representation.vertex_list)-1
                        and len(i_current_ant.pendindg_dests) > 1)):
                #The car is not ready or is already added to the solution
                continue

            found = False

            for current_reachable_id in reachable_cars:
                current_reachable = self.representation.vertex_list[current_reachable_id]

                if (current_reachable.line_id == current_to_car.line_id
                        and current_reachable.arrival_time < current_to_car):
                    found = True
                    break

            if not found:
                reachable_cars.append(current_to_car_id)

        return reachable_cars

    def select_next_node(self, i_current_ant, i_possible_dests):
        """Checks the transaction rule to select the next node in the path"""

        rd_q_value = rd.random()

        if rd_q_value <= self.q_value:
            selected_node = self.explotation(i_current_ant, i_possible_dests)
        else:
            selected_node = self.exploration(i_current_ant, i_possible_dests)

        return selected_node

    def explotation(self, i_current_ant, i_possible_dests):
        """Calculates next node by explotation"""
        calculated_values = []
        current_car = i_current_ant.current_car
        selected = -1
        counter = 0

        for current_dest_id in i_possible_dests:
            current_pheromone = self.pheromone_values[current_car][current_dest_id]

            solution_path = i_current_ant.current_solution[:]
            solution_path.append(current_dest_id)
            current_weight = (self.get_path_value(solution_path) - i_current_ant.current_solution_value + 1) ** -1

            current_value = current_pheromone * (current_weight ** self.b_value)
            calculated_values.append(current_value)

        for current_cal_value in calculated_values:
            if selected == -1 or current_cal_value > calculated_values[selected]:
                selected = counter

            counter += 1

        return i_possible_dests[selected]

    def exploration(self, i_current_ant, i_possible_dests):
        """Calculates next node by exploration"""
        calculated_values = []
        current_car = i_current_ant.current_car
        calculated_sum = 0

        for current_dest_id in i_possible_dests:
            current_pheromone = self.pheromone_values[current_car][current_dest_id]

            solution_path = i_current_ant.current_solution[:]
            solution_path.append(current_dest_id)
            current_weight = (self.get_path_value(solution_path) - i_current_ant.current_solution_value + 1) ** -1

            current_value = current_pheromone * (current_weight ** self.b_value)
            calculated_values.append(current_value)
            calculated_sum += current_value

        selected = self.select_from_probabilities(calculated_values, calculated_sum)

        return i_possible_dests[selected]

    def select_from_probabilities(self, i_values_list, i_total_value):
        """Given a calculated values vector and the total value, selects one index of the list
           due to the calculated probability"""
        calculated_probabilities = []
        previous_value = 0
        counter = 0

        for current_value in i_values_list:
            calculated_value = (current_value / i_total_value) + previous_value
            previous_value = calculated_value
            calculated_probabilities.append(calculated_value)

        rd_value = rd.random()

        for current_prob in calculated_probabilities:
            if rd_value <= current_prob:
                return counter
            counter += 1

    def get_path_value(self, i_path_list):
        """Gets the length of a path"""
        path_value = 0
        counter = 0
        previous_car_id = 0

        for current_car_id in i_path_list:
            if counter > 0:
                current_car = self.representation.vertex_list[current_car_id]
                current_weight = self.representation.weight_matrix[previous_car_id][current_car_id]

                if current_weight == 0 and current_car.line_id != 'E':
                    if self.check_line_in_use(i_path_list, counter):
                        current_weight = 2

                if current_car.arrival_time > path_value + current_weight:
                    path_value = current_car.arrival_time
                else:
                    path_value += current_weight

            previous_car_id = current_car_id
            counter += 1

        return path_value

    def check_line_in_use(self, i_path_list, i_current_idx):
        """Checks if a car entering with value 0, can enter immediatly or has to wait d time"""
        current_car_idx = i_path_list[i_current_idx]
        current_car = self.representation.vertex_list[current_car_idx]
        current_line = self.inner_data.get_line_by_id(current_car.line_id)
        non_conflict = current_line.non_confl_lines[:]

        if len(non_conflict) == 0:
            return False

        if i_current_idx >= len(non_conflict):
            for current_i in range(i_current_idx - len(non_conflict), i_current_idx):
                previous_car_id = i_path_list[current_i]
                previous_car = self.representation.vertex_list[previous_car_id]

                if previous_car.line_id in non_conflict:
                    non_conflict.remove(previous_car.line_id)

        if len(non_conflict) == 0:
            return True

        return False

    def local_pheromone_update(self, i_from_car_id, i_to_car_id):
        """Local pheromone update"""
        w_updated = self.pheromone_values[i_from_car_id][i_to_car_id]
        w_updated = ((1 - self.p_value) * w_updated) + (self.p_value * self.pherom_ini_value)
        self.pheromone_values[i_from_car_id][i_to_car_id] = w_updated

    def global_pheromone_update(self, i_best_ant_id):
        """Global pheromone update with"""
        self.pheromone_values = self.pheromone_values * (1 - self.a_value)
        counter = 0
        best_ant = self.ant_status[i_best_ant_id]
        previous_car_id = 0

        for current_car_id in best_ant.current_solution:
            if counter == 0:
                continue

            w_updated = self.pheromone_values[previous_car_id][current_car_id]
            w_updated = w_updated + (self.a_value + (best_ant.current_solution_value ** -1))

            previous_car_id = current_car_id

    def get_best_ant(self):
        """Returns the index of the best ant"""
        current_best = -1
        counter = 0

        for current_ant in self.ant_status:
            if (current_best == -1 or
                    current_ant.current_solution_value < self.ant_status[current_best].current_solution_value):
                current_best = counter

            counter += 1

        return current_best

    def convert_solution(self, sol_vector):
        """Returns the solution in a cars vaector"""

        sol_indexes = sol_vector[1:len(sol_vector) - 1]
        cars_sol = []

        for current_idx in sol_indexes:
            cars_sol.append(self.representation.vertex_list[current_idx])

        return cars_sol
