#!/usr/bin/python3

import sys
import os
import time
from datetime import datetime as dt


os.chdir(os.environ['HOME'] + '/time_manager')

SEC_IN_DAY = 86_400
SEC_IN_HOUR = 3_600

TIME_FORMAT_PATTERN = '%a %F %T'

def run(name, command, timeframe=None):
    '''Run main program'''
    # checks to see if the directory 'name' exists,
    # and if it doesn't it creates the dir
    if not os.path.isdir(name):
        os.mkdir(name)

    os.chdir(name)

    # checks to see if the data.csv file exists,
    # and if it doesn't, it creates the file
    if not os.path.isfile('data.csv'):
        with open('data.csv', 'w') as f:
            f.write('START,STOP\n')

    if command == 'START':
        start()
    elif command == 'STOP':
        stop()
    elif command == 'UNDO':
        undo()
    elif command == 'VIEW':
        view(timeframe)


def start():
    '''Add start time'''
    with open('data.csv', 'a') as f:
        f.write(str(int(time.time())) + ',')


def stop():
    '''Add stop time'''
    with open('data.csv', 'a') as f:
        f.write(str(int(time.time())) + '\n')


def undo():
    '''Delete last start/stop time added'''
    with open('data.csv') as f:
        lines = f.readlines()

    data = lines[:-1]
    last_line = lines[-1]

    if last_stop(last_line):
        # last_line.split(',')[0] is start time of last_line
        data.append(last_line.split(',')[0] + ',')

    # rewrite data.csv with all the previous data
    # except the last start/stop time
    with open('data.csv', 'w') as f:
        for line in data:
            f.write(line)

def last_stop(line):
    '''Determine if last time added to line was a stop time'''
    return line[-1] == '\n'

def last_start(line):
    '''Determine if last time added to line was a start time'''
    return line[-1] == ','

def view(timeframe):
    '''Output data and summaries for logged time'''
    with open('data.csv') as f:
        lines = [line.strip().split(',') for line in f.readlines()[1:]]
    # show everything if timeframe was not specified,
    # otherwise only data for the past [timeframe] days.
    if timeframe is None:
        timeframe = (int(lines[-1][0]) - int(lines[0][0])) / SEC_IN_DAY

    timeframe = int(timeframe)
    if timeframe == 0:
        timeframe = 1
    timeframe_seconds = SEC_IN_DAY * timeframe
    min_seconds = int(time.time()) - timeframe_seconds
    data = [[int(sec) for sec in line]  # maps ['start', 'stop'] to ints
            for line in lines
            if int(line[0]) >= min_seconds]  # selects in timeframe

    diffs = [stop - start for start, stop in data]
    avg_hrs_per_day = float(sum(diffs)) / timeframe / SEC_IN_HOUR
    for start, stop in data:
        print(f'Started: {to_datetime(start)}')
        print(f'Stopped: {to_datetime(stop)}\n')
    print(f'You studied an average of {avg_hrs_per_day:.2f} hours per day '\
          f'for the past {timeframe} day(s).')


def to_datetime(sec):
    '''Convert total seconds to friendly strftime datetime format'''
    return dt.fromtimestamp(sec).strftime(TIME_FORMAT_PATTERN)


def display_help():
    '''Output help.txt to the console'''
    with open('help.txt') as f:
        print(f.read())


def is_help(arg):
    '''Check if command supplied is a help command'''
    return (arg == 'HELP' or
            arg == '-H' or
            arg == '--HELP')


def is_view(args):
    '''Check if command supplied is a view command'''
    return len(args) >= 2 and args[1] == 'VIEW'


def is_all_alpha(name):
    '''Check if name supplied is only made of letters'''
    return all([char.isalpha() for char in name])


def is_invalid_command(command):
    '''Check if command is none of the valid 4 commands'''
    return (command != 'START' and
            command != 'STOP' and
            command != 'UNDO' and
            command != 'VIEW')


def is_valid(args):
    '''Check if format of arguments is correct as specified in help.txt'''
    # if the command is VIEW and it has a total of 2 or 3
    # args ({name, view, [n]}), then its a valid command
    if is_view(args) and (len(args) == 3 or len(args) == 2):
        return True

    # if less than or more than 2 arguments supplied
    # (ex. {JOHN} or {JOHN START EXTRA_ARG}), then the command
    # does not follow proper format
    elif len(args) != 2:
        return False

    # if the command is not one of the supported 4, then it is invalid
    elif is_invalid_command(args[1]):
        return False

    # if the name has anything other than letters, it's invalid
    elif not is_all_alpha(args[0]):
        return False
    else:
        return True


if __name__ == "__main__":
    # gets the arguments passed in when run as a script/command
    # (ex. ./time_manager.py NAME START/STOP/UNDO/VIEW [N])
    args = [arg.upper() for arg in sys.argv[1:]]

    # checks whether to display help or to run the script
    if not is_valid(args) or is_help(args[0]):
        display_help()
    else:
        run(*args)
