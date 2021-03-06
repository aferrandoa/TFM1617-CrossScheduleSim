"""Constants"""
#APP CONTROL
RUN_CONTROL = 1
#TRAFFIC LIGHT ON = 1
USE_TRAFFIC_LIGHT = 1
#CAR ADD MODE R:Randon F:File
CAR_ADD_MODE = 'F'
#RANDOM FRECUENCY
RANDOM_RATE = 0.4

#Pixels per meter
CURRENT_ID = 0
APP_SCALE = 9.55
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
YELLOW = (250, 250, 0)
LINE_WIDTH = 30
CONTROL_WIDTH = 10
CONTROL_DISTANCE = 150
CAR_LENGTH = 42
CAR_WIDTH = 19

#Car status
FREE_ROAD = 'F'     #Out of the control zone
CONTROLLED = 'CO'   #Under control
CROSSING = 'CR'     #Inside the danger zone
OUT = 'O'           #Left the danger zone

#ANT COLONY
PARAM_D = 2
PARAM_S = 6
ANT_NUMBER = 5
ITERATIONS_NUMBER = 5
Q_VALUE = 0.1
B_VALUE = 3
P_VALUE = 0.1
A_VALUE = 0.3

#TRAFFIC LIGHT
INTERVAL = 10000

#LOGGING FILE
REP_FILE_NAME = 'experiments/LOGS_REP.out'
REPFILE = open(REP_FILE_NAME, 'r')
REPFILE_LINES = REPFILE.readlines() 
CURRENT_LINE = 0

LOG_FILE_NAME = 'experiments/LOGS.out'
LOGSFILE = open(LOG_FILE_NAME, 'w')
LOGSFILE.write('INI;ANT_NUMBER:' + str(ANT_NUMBER) + '\n')
LOGSFILE.write('INI;ITERATIONS_NUMBER:' + str(ITERATIONS_NUMBER) + '\n')
LOGSFILE.write('INI;Q_VALUE:' + str(Q_VALUE) + '\n')
LOGSFILE.write('INI;B_VALUE:' + str(B_VALUE) + '\n')
LOGSFILE.write('INI;P_VALUE:' + str(P_VALUE) + '\n')
LOGSFILE.write('INI;A_VALUE:' + str(A_VALUE) + '\n')
