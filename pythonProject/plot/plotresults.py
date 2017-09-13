"""PLOT MODULE"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Slider

mode = 'Change'
modes = ('Change', 'Cars Num', 'Time')
interval = 5

def update(event):
    """Updates the plot"""

    plt.clf()
    main()

def update_radio(event):
    """Updates the plot"""
    global mode
    mode = event
    #print mode
    plt.clf()
    main()

def update_slider(event):
    """Updates the slider interval"""
    
    global interval
    interval = round(event)

def main():
    """Main function"""

    if mode == 'Change':
        loadaxes_chg()
        plt.xlabel('Parameter changes')
    elif mode == 'Cars Num':
        loadaxes_carnum('./gui/experiments/LOGS_REP.out', 'b', 'solid')
        loadaxes_carnum('./gui/experiments/LOGS.out', 'r', '--')
        plt.xlabel('Cars interval')
    else:
        loadaxes_time('./gui/experiments/LOGS_REP.out', 'b', '-')
        loadaxes_time('./gui/experiments/LOGS.out', 'r', '--')
        plt.xlabel('Time interval')
        
    plt.ylabel('Average wait time')
    #plt.xlabel(changelabels)

    axnext = plt.axes([0.05, 0.9, 0.1, 0.05])
    bnref = Button(axnext, 'Refresh')
    bnref.on_clicked(update)
    
    axnext = plt.axes([0.1, 0.87, 0.3, 0.1], frameon=False ,aspect='equal')
    radio = RadioButtons(axnext, modes)
    radio.on_clicked(update_radio)
    radio.eventson = False
    radio.set_active(modes.index(mode))
    radio.eventson = True

    axnext = plt.axes([0.5, 0.87, 0.3, 0.1], frameon=False ,aspect='equal')
    slider = Slider(axnext, 'Interval', 1, 50, valinit=interval, valfmt='%1.0f')
    slider.on_changed(update_slider)

    plt.show()

def loadaxes_chg():
    """Loads the plotaxes"""

    filename = './gui/experiments/LOGS.out'
    endini = 0
    acum = 0.0
    counter = 0
    waittimes = []
    changes = []
    changescount = 0
    changelabels = []

    with open(filename) as f:
        content = f.readlines()

    for currentline in content:
        #INI PARAMETERS LINES
        if endini == 0:
            if currentline.startswith('INI'):
                #print currentline
                continue
            else:
                endini = 1

        #VALUES LINES
        if currentline.startswith('CHANGE'):
            if counter > 0:
                #print currentline
                waittimes.append(acum / counter)
                changescount += 1
                changes.append(changescount)
                acum = 0.0
                counter = 0
        else:
            timevalue = currentline.split(':')[1]
            acum += float(timevalue)
            counter += 1.0

    if counter > 0:
        waittimes.append(acum / counter)
        changescount += 1
        changes.append(changescount)

    plt.plot(changes, waittimes, 'r')
    plt.xticks(changes)

def loadaxes_carnum(filename, color, linemode):
    """Loads the plotaxes"""

    endini = 0
    acum = 0.0
    counter = 0
    waittimes = []
    changes = []
    changescount = 0
    changelabels = []

    with open(filename) as f:
        content = f.readlines()

    for currentline in content:
        #INI PARAMETERS LINES
        if endini == 0:
            if currentline.startswith('INI'):
                #print currentline
                continue
            else:
                endini = 1

        #VALUES LINES
        if not currentline.startswith('CHANGE'):
            if counter >= interval:
                changescount+=1
                waittimes.append(acum / counter)
                changes.append(changescount)
                acum = 0.0
                counter = 0

            timevalue = currentline.split(':')[1]
            acum += float(timevalue)
            counter += 1.0

    if counter > 0:
        waittimes.append(acum / counter)
        changescount += 1
        changes.append(changescount)

    plt.plot(changes, waittimes, color = color, linestyle = linemode)
    plt.xticks(changes)

def loadaxes_time(filename, color, linemode):
    """Loads the plotaxes"""

    endini = 0
    acum = 0.0
    counter = 0
    waittimes = []
    changes = []
    changescount = 0
    changelabels = []
    last_period = 0

    with open(filename) as f:
        content = f.readlines()

    for currentline in content:
        #INI PARAMETERS LINES
        if endini == 0:
            if currentline.startswith('INI'):
                #print currentline
                continue
            else:
                endini = 1

        #VALUES LINES
        if not currentline.startswith('CHANGE'):

            entrytime = int(currentline.split(':')[2]) + int(currentline.split(':')[1])
            current_period = int(entrytime) // (interval*1000)

            if current_period != last_period:

                period_diff = current_period - last_period
                #print current_period
                if period_diff > 1:
                    for missed_per in range(int(last_period) + 1, int(current_period)):
                        changescount+=1
                        changes.append(changescount)
                        waittimes.append(-1)

                last_period = current_period
                changescount+=1

                if counter > 0:
                    waittimes.append(acum / counter)
                else:
                    waittimes.append(-1)

                changes.append(changescount)
                acum = 0.0
                counter = 0

            timevalue = currentline.split(':')[1]
            acum += float(timevalue)
            counter += 1.0

    if counter > 0:
        waittimes.append(acum / counter)
        changescount += 1
        changes.append(changescount)

    plt.plot(changes, waittimes, color = color, linestyle = linemode)
    plt.xticks(changes)

if __name__ == '__main__':
    main()
