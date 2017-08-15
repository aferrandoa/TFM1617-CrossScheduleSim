import sys
import pygame
sys.path.append('../')

from vo.Car import Car
from vo.InnerData import InnerData
from vo.Line import Line
import initialization.Initialization as init
import antColony.AntColonySystem as acs

import GuiConstants
from GuiUtil import *

class GuiCrossControl(object):
    """Class responsible of the cross control"""

    def __init__(self, cross):
        self.carlines = {'N':[], 'S':[], 'W':[], 'E':[]}
        self.non_conflict = {'N':['S'], 'S':['N'], 'W':['E'], 'E':['W']}
        self.cross = cross
        self.clock = pygame.time.Clock()
        self.last_check_time = pygame.time.get_ticks()
        self.solution = None
        self.carscrossing = []
        self.traffic_light = GuiConstants.USE_TRAFFIC_LIGHT
        self.light_direction = 'V'

    def check_control_entries(self, lines):
        """Sets the method to open and close lines"""

        if GuiConstants.USE_TRAFFIC_LIGHT == 1:
            self.light_control(lines)
        else:
            self.order_control(lines)

    def light_control(self, lines):
        """Uses a traffic  light to control traffic"""

        for current_line in lines:
            collide_rect = None

            if current_line.direction == 'N':
                collide_rect = self.cross.ncontrol
            elif current_line.direction == 'S':
                collide_rect = self.cross.scontrol
            elif current_line.direction == 'E':
                collide_rect = self.cross.econtrol
            elif current_line.direction == 'W':
                collide_rect = self.cross.wcontrol

            for current_car in current_line.cars:
                if current_car.is_block:
                    continue

                #FREE ROAD TO CONTROLLED
                if (current_car.status == FREE_ROAD and
                        collide_rect.colliderect(current_car.rect)):
                    current_car.status = CONTROLLED
                    current_car.tickcarclock()
                    self.carlines[current_line.direction].append(current_car)
                    continue

                #CONTROLLED TO CROSSING
                if (current_car.status == CONTROLLED and
                        self.cross.crossrect.colliderect(current_car.rect)):
                    current_car.status = CROSSING
                    self.carscrossing.append(current_car)
                    continue

                #CROSSING TO OUT
                if (current_car.status == CROSSING and
                        not self.cross.crossrect.colliderect(current_car.rect)):
                    current_car.status = OUT
                    timespent = current_car.tickcarclock()
                    GuiConstants.LOGSFILE.write(str(current_car.ident) + ':' + str(timespent) + ':' + str(current_car.entry_time) + '\n')
                    GuiConstants.LOGSFILE.flush()
                    os.fsync(GuiConstants.LOGSFILE.fileno())
                    self.carlines[current_line.direction].remove(current_car)
                    self.carscrossing.remove(current_car)
                    continue
       
        self.close_all_lines(lines)

        for current_line in lines:
            if (((current_line.direction == 'N' or current_line.direction == 'S') and self.light_direction == 'V') or
                ((current_line.direction == 'W' or current_line.direction == 'E') and self.light_direction == 'H')):
                current_line.remove_block_car()

        current_time = pygame.time.get_ticks()

        if current_time - self.last_check_time > GuiConstants.INTERVAL:
            self.last_check_time = current_time
           
            if self.light_direction == 'V':
                self.light_direction = 'H'
            else:
                self.light_direction = 'V'

    def order_control(self, lines):
        """Updates the cars status depending their positions depending on the cross control areas"""

        recalculate = False

        for current_line in lines:
            collide_rect = None

            if current_line.direction == 'N':
                collide_rect = self.cross.ncontrol
            elif current_line.direction == 'S':
                collide_rect = self.cross.scontrol
            elif current_line.direction == 'E':
                collide_rect = self.cross.econtrol
            elif current_line.direction == 'W':
                collide_rect = self.cross.wcontrol

            for current_car in current_line.cars:
                if current_car.is_block:
                    continue

                #FREE ROAD TO CONTROLLED
                if (current_car.status == FREE_ROAD and
                        collide_rect.colliderect(current_car.rect)):
                    current_car.status = CONTROLLED
                    current_car.tickcarclock()
                    self.carlines[current_line.direction].append(current_car)
                    recalculate = True
                    continue

                #CONTROLLED TO CROSSING
                if (current_car.status == CONTROLLED and
                        self.cross.crossrect.colliderect(current_car.rect)):
                    current_car.status = CROSSING
                    self.carscrossing.append(current_car)
                    self.close_all_lines(lines)
                    self.solution.remove(self.solution[0])
                    continue

                #CROSSING TO OUT
                if (current_car.status == CROSSING and
                        not self.cross.crossrect.colliderect(current_car.rect)):
                    current_car.status = OUT
                    timespent = current_car.tickcarclock()
                    GuiConstants.LOGSFILE.write(str(current_car.ident) + ':' + str(timespent) + ':' + str(current_car.entry_time) + ':' + current_line.direction + '\n')
                    GuiConstants.LOGSFILE.flush()
                    os.fsync(GuiConstants.LOGSFILE.fileno())
                    self.carlines[current_line.direction].remove(current_car)
                    self.carscrossing.remove(current_car)
                    continue

        if recalculate:
            data = self.prepare_data()
            self.close_all_lines(lines)
            self.solution = self.calculate_order(data)
            #self.start_control(lines)

        self.check_next_car(lines)

    def prepare_data(self):
        """Prepares data for the ant colony"""

        data = InnerData(PARAM_D, PARAM_S)

        #NORTH LINE
        self.add_line_to_data(data, 1, 'N', 2)
        #SOUTH LINE
        self.add_line_to_data(data, 2, 'S', 1)
        #WEST LINE
        self.add_line_to_data(data, 3, 'W', 4)
        #WEST LINE
        self.add_line_to_data(data, 4, 'E', 3)

        return data

    def add_line_to_data(self, data, line_id, direction, non_conflict):
        """Adds a line to the inner data"""

        nline = Line(line_id)
        nline.add_non_conflict(line_id)
        nline.add_non_conflict(non_conflict)
        data.add_line(nline)
        car_counter = 1

        for current_car in self.carlines[direction]:
            if current_car.status == CONTROLLED:
                arrive_time = round(distance_rects(current_car.rect, self.cross.crossrect)/10)
                #print('car: %d, arrive: %d', current_car.ident, arrive_time)

                data.add_car(Car(car_counter, line_id, arrive_time))
                car_counter += 1

    def calculate_order(self, inner_data):
        """Calculates the car order using the colony system"""

        representation = init.create_repesentation(inner_data)
        #ini_pherom_value = init.calculate_ini_pheromone(representation, inner_data)
        ini_pherom_value = 25
        acs_process = acs.AntColonySystem(inner_data, representation, GuiConstants.ANT_NUMBER, ini_pherom_value,
                                          GuiConstants.ITERATIONS_NUMBER, GuiConstants.Q_VALUE, GuiConstants.B_VALUE,
                                          GuiConstants.P_VALUE, GuiConstants.A_VALUE)
        acs_process.initialize()
        solution = acs_process.run()
        return solution

    def close_all_lines(self, lines):
        """Closes all the lines"""

        for current_line in lines:
            if current_line.direction == 'N':
                block_pos = (current_line.position[0], self.cross.crossrect.bottomright[1] - GuiConstants.CAR_LENGTH)    
                current_line.add_block_car(block_pos)
            elif current_line.direction == 'S':
                block_pos = (current_line.position[0], self.cross.crossrect.topright[1])
                current_line.add_block_car(block_pos)
            elif current_line.direction == 'W':
                block_pos = (self.cross.crossrect.topright[0] - GuiConstants.CAR_LENGTH, self.cross.crossrect.topright[1])
                current_line.add_block_car(block_pos)
            elif current_line.direction == 'E':
                block_pos = (self.cross.crossrect.bottomleft[0], self.cross.crossrect.topright[1] + LINE_WIDTH)
                current_line.add_block_car(block_pos)

    def open_all_lines(self, lines):
        """Opens all lines"""

        for current_line in lines:
            current_line.remove_block_car()

    def get_line_from_car(self, line_id, lines):
        """Gets the line object from the cars line_id"""

        if line_id == 1:
            return lines[0]
        elif line_id == 2:
            return lines[1]
        elif line_id == 3:
            return lines[3]
        elif line_id == 4:
            return lines[2]

    def start_control(self, lines):
        """Starts the cars control"""

        if self.carscrossing == 0 and len(self.solution) > 0:
            first_car = self.solution[0]
            prev_line = self.get_line_from_car(first_car.line_id, lines)

            prev_line.remove_block_car()
            self.solution.remove(first_car)

            if len(self.solution) > 0:
                next_car = self.solution[0]
                next_line = self.get_line_from_car(next_car.line_id, lines)

                if next_line.direction in self.non_conflict[prev_line.direction]:
                    next_line.remove_block_car()
                    self.solution.remove(next_car)

    def check_next_car(self, lines):
        """Checks if next car can cross"""

        if self.solution is None:
            return

        rest_cars = len(self.solution)

        if rest_cars == 0:
            self.open_all_lines(lines)
        else:
            car_to_cross = self.solution[0]
            next_line = self.get_line_from_car(car_to_cross.line_id, lines)
            cars_crossing_nbr = len(self.carscrossing)

            if cars_crossing_nbr > 0:
                last_car_crossing = self.carscrossing[cars_crossing_nbr - 1]
                line_crossing = self.get_line_from_car(self.get_line_id_from_dir(last_car_crossing.direction), lines)
                
                if next_line.direction == line_crossing.direction or next_line.direction in self.non_conflict[line_crossing.direction]:
                    next_line.remove_block_car()
            else:
                next_line.remove_block_car()

    def get_line_id_from_dir(self, direction):
        """Gets the line id from the direction"""

        if direction == 'N':
            return 1
        elif direction == 'S':
            return 2
        elif direction == 'W':
            return 3
        elif direction == 'E':
            return 4
