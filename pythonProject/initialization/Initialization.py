"""Functions to initialize the data"""
import numpy as np

from vo.Car import Car
from vo.InnerData import InnerData
from vo.Line import Line
from vo.Representation import Representation

def get_inner_data(i_file_name):
    """Gets the data from the inner file"""

    r_file = open(i_file_name, 'r')

    r_file.readline()
    #Read comment line
    values_string = r_file.readline()

    list_ds = values_string.strip('\n').split(';')
    inner_data = InnerData(list_ds[0], list_ds[1])

    #Read comment line
    values_string = r_file.readline()

    readed_lines = r_file.readlines()

    for current in readed_lines:
        line_blocks = current.strip('\n').split('#')
        current_line = Line(line_blocks[0])
        current_line.add_non_conflict(current_line.line_id)

        non_conflict_list = line_blocks[2].split(';')

        for current_no_conflict in non_conflict_list:
            current_line.add_non_conflict(current_no_conflict)

        inner_data.add_line(current_line)

        line_cars_list = line_blocks[1].split(';')
        car_counter = 1

        for current_car in line_cars_list:
            inner_data.add_car(Car(car_counter, current_line.line_id, current_car))
            car_counter += 1

    r_file.close()

    return inner_data

def create_repesentation(i_inner_data):
    """Create an object with the matrix represting the problem"""
    vertex_list = []
    initial_vertex_list = []
    end_vertex_list = []
    edge_list = []
    weight_matrix = np.zeros((len(i_inner_data.car_list) + 2, (len(i_inner_data.car_list) + 2)))
    car_counter = 1
    previous_line = 0

    #Add ini vertex
    ini_vertex = Car(0, 'I', 0)
    vertex_list.append(ini_vertex)

    for current_car in i_inner_data.car_list:
        vertex_list.append(current_car)
        current_edge_list = []
        car_line = i_inner_data.get_line_by_id(current_car.line_id)

        if car_counter == 1:
            previous_line = current_car.line_id
        elif previous_line != current_car.line_id:
            end_vertex_list.append(car_counter - 1)
            previous_line = current_car.line_id


        #Check initial node
        if int(current_car.car_id) == 1:
            initial_vertex_list.append(car_counter)

        #Loop over possible target cars
        to_car_counter = 1

        for current_to_car in i_inner_data.car_list:
            #Same car
            if current_car.get_car_def == current_to_car.get_car_def:
                weight_matrix[car_counter][to_car_counter] = -1
            else:
                #Same line
                if current_car.line_id == current_to_car.line_id:
                    #Only the next car in the same line is added
                    if int(current_to_car.car_id) == int(current_car.car_id) + 1:
                        current_edge_list.append(to_car_counter)
                        weight_matrix[car_counter][to_car_counter] = i_inner_data.d_value
                    else:
                        weight_matrix[car_counter][to_car_counter] = -1
                else:
                    current_edge_list.append(to_car_counter)
                    #Check if the car is in a non conflicting line
                    if current_to_car.line_id in car_line.non_confl_lines:
                        weight_matrix[car_counter][to_car_counter] = 0
                    else:
                        weight_matrix[car_counter][to_car_counter] = i_inner_data.s_value

            to_car_counter += 1

        edge_list.append(current_edge_list)

        car_counter += 1

    end_vertex_list.append(car_counter - 1)

    #Add end vertex and fill edge_list
    end_vertex = Car(len(edge_list)-1, 'E', 0)
    vertex_list.append(end_vertex)
    edge_list.insert(0, initial_vertex_list)
    edge_list.append([])

    for current_end_node in end_vertex_list:
        edge_list[current_end_node].append(len(edge_list)-1)

    return Representation(vertex_list, edge_list, weight_matrix)

def check_full_conflict_lines(i_current_car, i_sequence_list, i_inner_data):
    """Checks if the non conflicts lines are full"""
    sequence_list = i_sequence_list[1:]

    current_line = i_inner_data.get_line_by_id(i_current_car.line_id)
    non_conflict_lines = current_line.non_confl_lines[:]

    total_check_lines = len(non_conflict_lines)
    len_sequence = len(sequence_list)

    if len_sequence >= total_check_lines:
        cars_to_check = sequence_list[-total_check_lines:]

        for current_car in cars_to_check:
            if current_car.line_id in non_conflict_lines:
                non_conflict_lines.remove(current_car.line_id)
            else:
                return False
    else:
        return False

    return True

def calculate_ini_pheromone(i_representation, i_inner_data):
    """Calculates the ini pheromone value"""

    sequence_result = []
    pending_cars = i_representation.vertex_list[:]
    all_car_list = i_representation.vertex_list[:]
    current_time = 0
    current_car = pending_cars[0]
    sequence_result.append(current_car)
    pending_cars.remove(current_car)

    while len(pending_cars) > 0:
        car_index = all_car_list.index(current_car)
        possible_dest = i_representation.edge_list[car_index]
        minimum_time = float("inf")
        selected_car = None
        car_no_conflict = False
        current_non_conflict = []

        if current_car.line_id != 'I':
            car_line = i_inner_data.get_line_by_id(current_car.line_id)
            current_non_conflict = car_line.non_confl_lines

        for current_dest in possible_dest:
            to_car = all_car_list[current_dest]

            if to_car not in pending_cars:
                continue

            if to_car.line_id == 'E':
                if len(pending_cars) > 1:
                    continue
                else:
                    sequence_result.append(to_car)
                    pending_cars.remove(to_car)
                    continue

            current_weight = i_representation.weight_matrix[car_index][current_dest]

            if current_time + current_weight >= to_car.arrival_time:

                if to_car.line_id in current_non_conflict:
                    if (current_weight == 0
                            and not check_full_conflict_lines(to_car, sequence_result,
                                                              i_inner_data)):
                        if ((selected_car is None or not car_no_conflict)
                                or to_car.arrival_time < selected_car.arrival_time):
                            minimum_time = current_weight
                            selected_car = to_car
                            car_no_conflict = True

                    elif (current_weight == i_inner_data.d_value):
                          #and not check_full_conflict_lines(to_car, sequence_result,
                          #                              i_inner_data)):
                        minimum_time = current_weight
                        selected_car = to_car
                        car_no_conflict = True

                else:
                    if (selected_car is None or (to_car.arrival_time < selected_car.arrival_time
                                                 and current_weight < minimum_time)):
                        minimum_time = current_weight
                        selected_car = to_car
                        car_no_conflict = False

        if selected_car != None:
            sequence_result.append(selected_car)
            current_car = selected_car
            pending_cars.remove(selected_car)
            current_time += minimum_time
        else:
            current_time += 1

    #print 'Current time ' + str(current_time - 1)
    #print sequence_result
    return current_time - 1
