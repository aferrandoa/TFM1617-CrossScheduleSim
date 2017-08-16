"""Main GUI class"""
import sys
import pygame
import random
from GuiLine import *
from GuiCross import *
from GuiCrossControl import *
import GuiConstants
from pgu import gui

def log_constant_change(constant, value):
    """Logs a constant change"""
    GuiConstants.LOGSFILE.write('CHANGE;' + constant + ':' + str(value) + '\n')
    GuiConstants.LOGSFILE.flush()
    os.fsync(GuiConstants.LOGSFILE.fileno())

def toggle_run_control():
    """Toggle run control callback"""
    if GuiConstants.RUN_CONTROL == 1:
        GuiConstants.RUN_CONTROL = 0
    else:
        GuiConstants.RUN_CONTROL = 1

def toggle_trlight(toggle_in):
    """Change toggle traffic light"""
    if toggle_in.value:
        GuiConstants.USE_TRAFFIC_LIGHT = 1
    else:
        GuiConstants.USE_TRAFFIC_LIGHT = 0
        
    log_constant_change('TR_LIGHT', toggle_in.value)

def chg_ant_number(sliderin, labelin):
    """Change ant number callback"""
    GuiConstants.ANT_NUMBER = sliderin.value
    labelin.value = str(GuiConstants.ANT_NUMBER)
    log_constant_change('ANT_NUMBER', GuiConstants.ANT_NUMBER)

def chg_iter_number(sliderin, labelin):
    """Change iterations number callback"""
    GuiConstants.ITERATIONS_NUMBER = sliderin.value
    labelin.value = str(GuiConstants.ITERATIONS_NUMBER)
    log_constant_change('ITERATIONS_NUMBER', GuiConstants.ITERATIONS_NUMBER)

def chg_q_value(sliderin, labelin):
    """Change q value callback"""
    GuiConstants.Q_VALUE = sliderin.value / 10.0
    labelin.value = str(GuiConstants.Q_VALUE)
    log_constant_change('Q_VALUE', GuiConstants.Q_VALUE)

def chg_a_value(sliderin, labelin):
    """Change a value callback"""
    GuiConstants.A_VALUE = sliderin.value / 10.0
    labelin.value = str(GuiConstants.A_VALUE)
    log_constant_change('A_VALUE', GuiConstants.A_VALUE)

def chg_p_value(sliderin, labelin):
    """Change p value callback"""
    GuiConstants.P_VALUE = sliderin.value / 10.0
    labelin.value = str(GuiConstants.P_VALUE)
    log_constant_change('P_VALUE', GuiConstants.P_VALUE)

def chg_b_value(sliderin, labelin):
    """Change b value callback"""
    GuiConstants.B_VALUE = sliderin.value
    labelin.value = str(GuiConstants.B_VALUE)
    log_constant_change('B_VALUE', GuiConstants.B_VALUE)

def chg_interval(sliderin, labelin):
    """Change the interval callback"""
    GuiConstants.INTERVAL = sliderin.value * 1000
    labelin.value = str(sliderin.value)
    log_constant_change('INTERVAL', GuiConstants.INTERVAL)

def chg_random_value(sliderin, labelin):
    """Change random rate callback"""
    GuiConstants.RANDOM_RATE = sliderin.value / 10.0
    labelin.value = str(GuiConstants.RANDOM_RATE)
    log_constant_change('RANDOM_V', GuiConstants.RANDOM_RATE)

def main():
    """Main function"""
    current_id = 0
    size = width, height = 1280, 1024
    green = (0, 250, 0)
    fps = 30
    timewarp = 1.0

    #init
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Crossroads test')

    #init GUI
    appgui = ini_gui()

    #Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(green)

    #Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Init lines
    lines = ini_lines(width / 2.0, height, width / 4.0, 0)
    lines2 = ini_lines(width / 2.0, height, (width - (width / 4.0)), 0)

    #Init crossroad and controller
    crossroad = GuiCross((width / 4.0, height / 2.0))
    crossroad2 = GuiCross((width - (width / 4.0), height / 2.0))
    cross_control = GuiCrossControl(crossroad)
    cross_control2 = GuiCrossControl(crossroad2)

    # Initialise clock
    clock = pygame.time.Clock()
    carsclock = pygame.time.Clock()
    carstime = 0
    appgui.paint()

    #Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GuiConstants.LOGSFILE.close()
                return
            if event.type == pygame.USEREVENT:
                add_car_event([lines, lines2], event.car)
            else:
                appgui.event(event)

        if GuiConstants.RUN_CONTROL == 0:
            continue

        #time operations
        clock.tick(fps)
        dt = timewarp / fps

        carstime += carsclock.tick()
        if  carstime > 200:
            select_cross = random.random()

            if select_cross > 0.5:
                current_id += check_add_car(lines, current_id, [0, 1, 2])
            else:
                current_id += check_add_car(lines2, current_id, [0, 1, 3])

            carstime = 0

        #Update logic
        for current_line in lines:
            current_line.update(dt)
        for current_line in lines2:
            current_line.update(dt)

        #Cross control
        cross_control.check_control_entries(lines)
        cross_control2.check_control_entries(lines2)

        #Draw objects
        for current_line in lines:
            current_line.draw()

        for current_line in lines2:
            current_line.draw()

        #Draw crossroad
        crossroad.draw()
        crossroad2.draw()

        for current_line in lines:
            current_line.render()

        for current_line in lines2:
            current_line.render()

        appgui.update()
        pygame.display.flip()

def ini_lines(width, height, posw, posh):
    """Initialize the lines"""
    lines = []
    lines.append(GuiLine('N', height, (posw, posh)))
    lines.append(GuiLine('S', height, (posw - LINE_WIDTH, posh)))
    lines.append(GuiLine('E', width, (posw - (width / 2.0), height / 2.0)))
    lines.append(GuiLine('W', width, (posw - (width / 2.0), (height / 2.0) - LINE_WIDTH)))

    return lines

def check_add_car(lines, current_id, allow_add):
    """Random car adder"""

    if GuiConstants.CAR_ADD_MODE == 'R':
        return check_add_car_random(lines, current_id, allow_add)
    else:
        return check_add_car_time(lines, current_id)

def check_add_car_random(lines, current_id, allow_add):
    """Random car adder"""
    chk_car = random.random()

    if chk_car > GuiConstants.RANDOM_RATE:
        select_line = random.random()
        allow_nbr = len(allow_add)
        mult_rdm = 1.0 / allow_nbr
        iter_nbr = 1

        for current_line in allow_add:
            if select_line < (mult_rdm * iter_nbr):
                lines[current_line].add_car(current_id)
                return 1

            iter_nbr += 1

    return 0

def check_add_car_time(lines, current_id):
    """Checks if a car form the rep file should be added"""

    current_time = pygame.time.get_ticks()
    check_next = True
    added_cars = 0

    while check_next:       
        if GuiConstants.CURRENT_LINE >= len(GuiConstants.REPFILE_LINES):
            return 0

        current_car = GuiConstants.REPFILE_LINES[GuiConstants.CURRENT_LINE]

        if not current_car.startswith('INI') and not current_car.startswith('CHANGE'):
            car_time = current_car.split(':')[2]
            car_id = current_car.split(':')[0]

            if int(car_time) <= current_time:
                car_dir = current_car.split(':')[3]
                car_dir = car_dir.replace('\n', '')

                if car_dir == 'N':
                    lines[0].add_car(car_id)
                elif car_dir == 'S':
                    lines[1].add_car(car_id)
                elif car_dir == 'E':
                    lines[2].add_car(car_id)
                elif car_dir == 'W':
                    lines[3].add_car(car_id)

                GuiConstants.CURRENT_LINE += 1
            else:
                check_next = False

        else:
            GuiConstants.CURRENT_LINE += 1

    return 0

def add_car_event(group_lines, car_inn):
    """Checks if an exit car is in the cars queue and adds it if needed"""

    for group in group_lines:
        for current_line in group:
            if current_line.rect.colliderect(car_inn.rect):
                current_line.add_car(car_inn)
                break


def ini_gui():
    """Initalizes GUI controls"""
    appgui = gui.App()
    appgui.connect(gui.QUIT, appgui.quit, None)
    #GUI container
    gui_container = gui.Container(align=-1, valign=-1)
    gui_table = gui.Table()
    #GIO STOP/RUN button
    gui_table.tr()
    btn_run = gui.Button("STOP/RUN")
    btn_run.connect(gui.CLICK, toggle_run_control)
    gui_table.td(btn_run)

    create_check(gui_table, "Traffic light", toggle_trlight)

    if GuiConstants.USE_TRAFFIC_LIGHT == 0:
        #GUI iterations number slider
        create_slider(gui_table, "Iterations number: ", GuiConstants.ITERATIONS_NUMBER, chg_iter_number, 5, 50)
        #GUI ants number slider
        create_slider(gui_table, "Ants number: ", GuiConstants.ANT_NUMBER, chg_ant_number, 5, 25)
        #GUI q value slider
        create_slider(gui_table, "q value: ", GuiConstants.Q_VALUE, chg_q_value, 0, 9, 10)
        #GUI a value slider
        create_slider(gui_table, "a value: ", GuiConstants.A_VALUE, chg_a_value, 0, 9, 10)
        #GUI p value slider
        create_slider(gui_table, "p value: ", GuiConstants.P_VALUE, chg_p_value, 0, 9, 10)
        #GUI b value slider
        create_slider(gui_table, "b value: ", GuiConstants.B_VALUE, chg_p_value, 0, 5)
    else:
        #Traffic light interval
        create_slider(gui_table, "Interval: ", GuiConstants.INTERVAL / 1000, chg_interval, 1, 20)

    #RANDOM RATE SLIDER
    create_slider(gui_table, "Car frecuency: ", GuiConstants.RANDOM_RATE, chg_random_value, 0, 9, 10)

    #Add table to GUI
    gui_container.add(gui_table, 0, 0)
    appgui.init(gui_container)

    return appgui

def create_slider(gui_table, ctrl_label, ctrl_value, ctrl_callback, ctrl_min, ctrl_max, ctrl_mult = 1):
    """Creates a slider to control a value"""
    gui_table.tr()
    gui_table.td(gui.Label(ctrl_label))
    txt = gui.Input(value=str(ctrl_value), width=30)
    gui_table.td(txt)
    slider = gui.HSlider(value=ctrl_value * ctrl_mult, min=ctrl_min, max=ctrl_max, size=20, width=120)
    slider.connect(gui.CHANGE, ctrl_callback, slider, txt)
    gui_table.td(slider)

def create_check(gui_table, ctrl_label, ctrl_callback):
    """Creates a checkbox to control a value"""

    cb1 = gui.Switch()
    cb1.connect(gui.CHANGE, ctrl_callback, cb1)
    cb1l = gui.Label(ctrl_label)
    gui_table.add(cb1)
    gui_table.add(cb1l)
    gui_table.tr()

if __name__ == '__main__':
    main()
