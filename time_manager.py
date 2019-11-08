#!/usr/bin/python3

import sys
import os
import time
from datetime import datetime as dt


os.chdir(os.environ['HOME'] + '/time_manager')

SEC_IN_DAY = 86_400
SEC_IN_HOUR = 3_600
SEC_IN_MIN = 60

TIME_FORMAT_PATTERN = '%a %Y-%m-%d %H:%M:%S'

FILE_DEST = 'data.psv'

DELIMETER = '|'
DELIM_REPLACEMENT = '^'
MESSAGE_DELIM = '%%'
EOL = '\n'


def run(name, command, *args):
    '''Run main program'''
    message = ''
    timeframe = None
    command = command.upper()
    name = name.upper()

    # checks to see if the directory f'{name}' exists,
    # and if it doesn't it creates the dir
    if not os.path.isdir(name):
        os.mkdir(name)

    os.chdir(name)

    # checks to see if the data.csv file exists,
    # and if it doesn't, it creates the file
    if not os.path.isfile(FILE_DEST):
        write([f'START{DELIMETER}STOP{EOL}'])

    if len(args) == 1:
        timeframe = args[0]
    elif len(args) == 2:
        message = args[1]

    if command == 'START':
        start(message)
    elif command == 'STOP':
        stop(message)
    elif command == 'UNDO':
        undo()
    elif command == 'VIEW':
        view(timeframe)


def start(message):
    '''Add start time'''
    message = message.replace(DELIMETER, DELIM_REPLACEMENT)
    with open(FILE_DEST) as f:
        assert last_stop(f.readlines()[-1]), "Cannot 'start' twice in a row!"
    with open(FILE_DEST, 'a') as f:
        f.write(f'{dt.now().strftime(TIME_FORMAT_PATTERN)}{MESSAGE_DELIM}{message}{DELIMETER}')


def stop(message):
    '''Add stop time'''
    message = message.replace(DELIMETER, DELIM_REPLACEMENT)
    with open(FILE_DEST) as f:
        assert last_start(f.readlines()[-1]), "Cannot 'stop' twice in a row!"
    with open(FILE_DEST, 'a') as f:
        f.write(f'{dt.now().strftime(TIME_FORMAT_PATTERN)}{MESSAGE_DELIM}{message}{EOL}')


def undo():
    '''Delete last start/stop time added'''
    lines = readlines()
    assert len(lines) > 1, "Cannot 'undo' anymore, reached max undo!"

    data = lines[:-1]
    last_line = lines[-1]

    if last_stop(last_line):
        data.append(last_line.split(DELIMETER)[0] + DELIMETER)

    # rewrite data.csv with all the previous data
    # except the last start/stop time
    write(data)


def view(timeframe):
    '''Output data and summaries for logged time'''
    err_msg = "Cannot 'view' on incomplete data! Please use the 'STOP' command"
    with open(FILE_DEST) as f:
        assert last_stop(f.readlines()[-1]), err_msg
    lines = [line.strip(EOL).split(DELIMETER) for line in readlines()[1:]]
    times = [[to_dt(start), to_dt(stop)] for start, stop in lines]

    timeframe = int(timeframe)

    diff_seconds = [(stop - start).seconds for start, stop in times]
    total_total_seconds = sum(diff_seconds)
    avg_total_seconds = total_total_seconds // timeframe

    display_lines(lines)
    display('Average', avg_total_seconds, ' per day')
    display('Total', total_total_seconds)


def display_lines(lines):
    ''''''
    for start, stop in lines:
        print(f'Start: {start}\nStop: {stop}')
        delta = to_dt(stop) - to_dt(start)
        display('Session time', delta.seconds, '\n')


def display(title, total_seconds, trailer=''):
    ''''''
    secs = total_seconds % SEC_IN_MIN
    mins = total_seconds // SEC_IN_MIN
    hours = total_seconds // SEC_IN_HOUR
    print(f'{title}: {hours:02}:{mins:02}:{secs:02}{trailer}')


def to_dt(string):
    ''''''
    return dt.strptime(string, TIME_FORMAT_PATTERN)


def readlines():
    ''''''
    with open(FILE_DEST) as f:
        return f.readlines()


def write(lines):
    ''''''
    with open(FILE_DEST, 'w') as f:
        for line in lines:
            f.write(line)


def last_stop(line):
    '''Determine if last time added to line was a stop time'''
    return line[-1] == EOL


def last_start(line):
    '''Determine if last time added to line was a start time'''
    return line[-1] == DELIMETER


def display_help():
    '''Output help.txt to the console'''
    with open('help.txt') as f:
        print(f.read())


def is_help(arg):
    '''Check if command supplied is a help command'''
    arg = arg.upper()
    return (arg == 'HELP' or
            arg == '-H' or
            arg == '--HELP')


def is_view(args):
    '''Check if valid view command'''
    return (len(args) == 2 or len(args) == 3) and args[1].upper() == 'VIEW'


def is_start(args):
    '''Check if valid start command'''
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'START'


def is_stop(args):
    '''Check if valid stop command'''
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'STOP'


def is_undo(args):
    '''Check if valid undo command'''
    return len(args) == 2 and args[1].upper() == 'UNDO'


def is_message(args):
    '''Check if message supplied with start/stop command'''
    return len(args) == 4 and args[2].upper() == '-M'


def is_all_alpha(name):
    '''Check if name supplied is only made of letters'''
    return all([char.isalpha() for char in name])


def is_valid(args):
    '''Check if format of arguments is correct as specified in help.txt'''

    return (is_start(args) or is_stop(args) or is_view(args) or is_undo(args)) and is_all_alpha(args[0])


if __name__ == "__main__":
    # gets the arguments passed in when run as a script/command
    # (ex. ./time_manager.py NAME START/STOP/UNDO/VIEW [N])
    args = sys.argv[1:]

    # checks whether to display help or to run the script
    if not is_valid(args) or is_help(args[0]):
        display_help()
    else:
        run(*args)
