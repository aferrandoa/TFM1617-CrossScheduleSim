"""Main class of the problem"""
import initialization.Initialization as init
import antColony.AntColonySystem as acs

ANT_NUMBER = 5
ITERATIONS_NUMBER = 5
Q_VALUE = 0.1
B_VALUE = 3
P_VALUE = 0.1
A_VALUE = 0.3
DATA_FILE_NAME = 'testData1.data'

print 'Initialization of data:'

INNER_DATA = init.get_inner_data(DATA_FILE_NAME)
print 'Data loaded from file "%s"' % DATA_FILE_NAME

REPRESENTATION = init.create_repesentation(INNER_DATA)
print 'Graph created'

INI_PHEROMONE_VALUE = init.calculate_ini_pheromone(REPRESENTATION, INNER_DATA)
print 'Ini pheromone value: %d' % INI_PHEROMONE_VALUE

ACS_PROCESS = acs.AntColonySystem(INNER_DATA, REPRESENTATION, ANT_NUMBER, INI_PHEROMONE_VALUE,
                                  ITERATIONS_NUMBER, Q_VALUE, B_VALUE, P_VALUE, A_VALUE)
ACS_PROCESS.initialize()
ACS_PROCESS.run()
