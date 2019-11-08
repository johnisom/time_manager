#!/usr/bin/python3

# Update the above shebang if that path does not
# exist on your system. Make sure that it points
# to a version of python 3.6 or greater.

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

FORBIDDEN = [DELIMETER, MESSAGE_DELIM, EOL]


def run(name: str, command: str, *args: list) -> None:
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


def sanitize(text: str) -> str:
    for forbidden in FORBIDDEN:
        text = text.replace(forbidden, DELIM_REPLACEMENT)
    return text


def start(message: str) -> None:
    '''Add start time'''
    message = sanitize(message)
    with open(FILE_DEST) as f:
        assert last_stop(f.readlines()[-1]), "Cannot 'start' twice in a row!"
    with open(FILE_DEST, 'a') as f:
        f.write(f'{dt.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{DELIMETER}')


def stop(message: str) -> None:
    '''Add stop time'''
    message = sanitize(message)
    with open(FILE_DEST) as f:
        assert last_start(f.readlines()[-1]), "Cannot 'stop' twice in a row!"
    with open(FILE_DEST, 'a') as f:
        f.write(f'{dt.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{EOL}')


def undo() -> None:
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


def view(timeframe: str or None) -> None:
    '''Output data and summaries for logged time'''
    err_msg = "Cannot 'view' on incomplete data! Please use the 'STOP' command"
    with open(FILE_DEST) as f:
        assert last_stop(f.readlines()[-1]), err_msg

    lines = []  # [[[entry, message], [entry, message]],
    #              [[entry, message], [entry, message]], etc.]
    for line in readlines()[1:]:
        start, stop = line.strip(EOL).split(DELIMETER)
        start = start.split(MESSAGE_DELIM)
        stop = stop.split(MESSAGE_DELIM)
        lines.append([start, stop])

    times = []  # [[datetime, datetime], [datetime, datetime], etc.]
    for start, stop in lines:
        start = to_dt(start[0])
        stop = to_dt(stop[0])
        times.append([start, stop])

    timeframe = int(timeframe)

    diff_seconds = [(stop - start).seconds for start, stop in times]
    total_total_seconds = sum(diff_seconds)
    avg_total_seconds = total_total_seconds // timeframe

    print(f'\nShowing results for the past {timeframe} day(s)\n')
    display_lines(lines, times)
    display('Average', avg_total_seconds, ' per day')
    display('Total', total_total_seconds)


def display_lines(lines: list, times: list) -> None:
    ''''''
    for idx, (start, stop) in enumerate(lines):
        start_message = start[1]
        stop_message = stop[1]
        if start_message:
            start_message = f' -> "{start_message}"'
        if stop_message:
            stop_message = f' -> "{stop_message}"'

        print(f'Start: {start[0]}{start_message}')
        print(f'Stop: {stop[0]}{stop_message}')
        delta = times[idx][1] - times[idx][0]
        display('Session time', delta.seconds, '\n')


def display(title: str, total_seconds: int, trailer: str = '') -> None:
    ''''''
    secs = total_seconds % SEC_IN_MIN
    mins = total_seconds // SEC_IN_MIN % SEC_IN_MIN
    hours = total_seconds // SEC_IN_HOUR % SEC_IN_MIN
    print(f'{title}: {hours:02}:{mins:02}:{secs:02}{trailer}')


def to_dt(string: str) -> dt:
    ''''''
    return dt.strptime(string, TIME_FORMAT_PATTERN)


def readlines() -> list:
    ''''''
    with open(FILE_DEST) as f:
        return f.readlines()


def write(lines: list) -> None:
    ''''''
    with open(FILE_DEST, 'w') as f:
        for line in lines:
            f.write(line)


def last_stop(line: str) -> bool:
    '''Determine if last time added to line was a stop time'''
    return line[-1] == EOL


def last_start(line: str) -> bool:
    '''Determine if last time added to line was a start time'''
    return line[-1] == DELIMETER


def display_help() -> None:
    '''Output help.txt to the console'''
    with open('help.txt') as f:
        print(f.read())


def is_help(arg: str) -> bool:
    '''Check if command supplied is a help command'''
    arg = arg.upper()
    return (arg == 'HELP' or
            arg == '-H' or
            arg == '--HELP')


def is_view(args: list) -> bool:
    '''Check if valid view command'''
    if len(args) == 3:
        if not is_valid_n(args[2]):
            return False
    return (len(args) == 2 or len(args) == 3) and args[1].upper() == 'VIEW'


def is_valid_n(arg: str) -> bool:
    '''Check N is integer greater than 0'''
    try:
        return int(arg) > 0
    except ValueError:
        return False

def is_start(args: list) -> bool:
    '''Check if valid start command'''
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'START'


def is_stop(args: list) -> bool:
    '''Check if valid stop command'''
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'STOP'


def is_undo(args: list) -> bool:
    '''Check if valid undo command'''
    return len(args) == 2 and args[1].upper() == 'UNDO'


def is_message(args: list) -> bool:
    '''Check if message supplied with start/stop command'''
    return len(args) == 4 and args[2].upper() == '-M'


def is_all_alpha(name: str) -> bool:
    '''Check if name supplied is only made of letters'''
    return all([char.isalpha() for char in name])


def is_valid(args: list) -> bool:
    '''Check if format of arguments is correct as specified in help.txt'''

    return (is_start(args) or is_stop(args) or
            is_view(args) or is_undo(args)) and is_all_alpha(args[0])


if __name__ == "__main__":
    # gets the arguments passed in when run as a script/command
    # (ex. ./time_manager.py NAME START/STOP/UNDO/VIEW [N])
    args = sys.argv[1:]

    # checks whether to display help or to run the script
    if not is_valid(args) or is_help(args[0]):
        display_help()
    else:
        run(*args)
