#!/usr/bin/python3

# Update the above shebang if that path does not
# exist on your system. Make sure that it points
# to a version of python 3.6 or greater.

import sys
import os
import time
from datetime import datetime, timedelta
from typing import Union, List, Optional


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


def run(name: str, command: str, *args: List[str]) -> None:
    '''Run main program'''
    message = ''
    timeframe_from = None
    timeframe_to = None
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
        timeframe_from = args[0]
    elif len(args) == 2:
        if args[0].upper() == '-M':
            message = args[1]
        else:
            timeframe_from = args[0]
            timeframe_to = args[1]

    if command == 'START':
        start(message)
    elif command == 'STOP':
        stop(message)
    elif command == 'UNDO':
        undo()
    elif command == 'VIEW':
        view(timeframe_from, timeframe_to)


def sanitize(text: str) -> str:
    '''Replace forbidden character sequences'''
    for forbidden in FORBIDDEN:
        text = text.replace(forbidden, DELIM_REPLACEMENT)
    return text


def start(message: str) -> None:
    '''Add start time'''
    if last_start(readlines()[-1]):
        print("Cannot 'start' twice in a row!")
        return
    message = sanitize(message)
    with open(FILE_DEST, 'a') as f:
        f.write(f'{datetime.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{DELIMETER}')


def stop(message: str) -> None:
    '''Add stop time'''
    if last_stop(readlines()[-1]):
        print("Cannot 'stop' twice in a row!")
        return
    message = sanitize(message)
    with open(FILE_DEST, 'a') as f:
        f.write(f'{datetime.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{EOL}')


def undo() -> None:
    '''Delete last start/stop time added'''
    lines = readlines()
    if len(lines) == 1:
        print("Cannot 'undo' anymore, reached max undo!")
        return
    data = lines[:-1]
    last_line = lines[-1]

    if last_stop(last_line):
        data.append(last_line.split(DELIMETER)[0] + DELIMETER)

    # rewrite data.csv with all the previous data
    # except the last start/stop time
    write(data)


def view(timeframe_from: Union[str, None], timeframe_to: Union[str, None]) -> None:
    '''Output data and summaries for logged time'''
    lines = get_split_lines()

    # Use current time as end time if no end time
    if last_start(readlines()[-1]):
        now_formatted = datetime.now().strftime(TIME_FORMAT_PATTERN)
        lines[-1][1] = [now_formatted, 'CURRENT']

    times = get_times(lines)
    if not times:
        print('No data to report')
        return

    if timeframe_from is None or timeframe_from == '_':
        timeframe_from = (times[-1][0] - times[0][0]).days + 1
    else:
        timeframe_from = int(timeframe_from)

    timeframe_to = 0 if timeframe_to is None else int(timeframe_to)

    idx_from, idx_to = indices_in_timeframe(
        times, *datetime_range(timeframe_from, timeframe_to))
    lines = lines[idx_from:idx_to]
    times = times[idx_from:idx_to]

    diff_seconds = [(stop - start).seconds for start, stop in times]
    total_total_seconds = sum(diff_seconds)
    avg_total_seconds = total_total_seconds // (timeframe_from - timeframe_to)

    display_timeframe(timeframe_from, timeframe_to)
    display_lines(lines, times)
    display('Average', avg_total_seconds, ' per day')
    display('Total', total_total_seconds)


def display_lines(lines: List[List[List[str]]],
                  times: List[List[datetime]]) -> None:
    '''Display start times, stop times, messages, and session times'''
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


def display(title: str, total_seconds: int,
            trailer: Optional[str] = '') -> None:
    '''Display line of time'''
    secs = total_seconds % SEC_IN_MIN
    mins = total_seconds // SEC_IN_MIN % SEC_IN_MIN
    hours = total_seconds // SEC_IN_HOUR % SEC_IN_MIN
    print(f'{title}: {hours:02}:{mins:02}:{secs:02}{trailer}')


def display_timeframe(timeframe_from: int, timeframe_to: int) -> None:
    '''Display info about timeframe'''
    if timeframe_to == 0:
        print(f'\nShowing results for the past {timeframe_from} day(s)\n')
    else:
        print(f'\nShowing results from {timeframe_from}', end=' ')
        print(f'days ago to {timeframe_to} day(s) ago\n')


def get_split_lines() -> List[List[List[str]]]:
    '''Get lines split into entry and message subcomponents'''
    lines = []
    # [[[entry, message], [entry, message]],
    #  [[entry, message], [entry, message]], etc.]
    for line in readlines()[1:]:
        start, stop = line.strip(EOL).split(DELIMETER)
        start = start.split(MESSAGE_DELIM)
        stop = stop.split(MESSAGE_DELIM)
        lines.append([start, stop])
    return lines


def get_times(lines: List[List[List[str]]]) -> List[List[datetime]]:
    '''From split lines create sublists of start and stop datetime objects'''
    # [[datetime, datetime], [datetime, datetime], etc.]
    times = []
    for start, stop in lines:
        start = to_datetime(start[0])
        stop = to_datetime(stop[0])
        times.append([start, stop])
    return times


def indices_in_timeframe(times: List[List[datetime]], datetime_from: datetime,
                         datetime_to: datetime) -> int:
    '''Find indices that selects times from timeframe_from to timeframe_to'''
    idx_from = 0
    idx_to = 0
    for start, end in times:
        if start < datetime_from:
            idx_from += 1
        if end < datetime_to:
            idx_to += 1
        else:
            break

    return idx_from, idx_to


def datetime_range(timeframe_from: int, timeframe_to: int) -> List[datetime]:
    '''Get the timeframe as 2 datetimes'''
    today = datetime.now().date()

    from_days_ago = today - timedelta(days=int(timeframe_from) - 1)
    to_days_ago = today - timedelta(days=int(timeframe_to))

    from_days_ago_datetime = datetime(from_days_ago.year,
                                      from_days_ago.month, from_days_ago.day)
    to_days_ago_datetime = datetime(to_days_ago.year, to_days_ago.month,
                                    to_days_ago.day, 23, 59, 59)
    return from_days_ago_datetime, to_days_ago_datetime


def to_datetime(string: str) -> datetime:
    '''Convert str to datetime'''
    return datetime.strptime(string, TIME_FORMAT_PATTERN)


def readlines() -> List[str]:
    '''Get data from data storage'''
    with open(FILE_DEST) as f:
        return f.readlines()


def write(lines: List[str]) -> None:
    '''Write data to data storage'''
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


def is_view(args: List[str]) -> bool:
    '''Check if valid view command'''
    if len(args) >= 3:
        if not is_valid_from(args[2]):
            return False
    if len(args) == 4:
        if not is_valid_to(args[3], args[2]):
            return False
    return (len(args) >= 2 and len(args) <= 4) and args[1].upper() == 'VIEW'


def is_valid_from(arg: str) -> bool:
    '''Check FROM is integer greater than 0 or underscore'''
    try:
        return arg == '_' or int(arg) > 0
    except ValueError:
        return False


def is_valid_to(to_arg: str, from_arg: str) -> bool:
    '''Check TO is integer 0 or greater'''
    try:
        if from_arg == '_':
            from_arg = int(to_arg) + 1
        else:
            from_arg = int(from_arg)
        return int(to_arg) >= 0 and int(to_arg) < from_arg
    except ValueError:
        return False


def is_start(args: List[str]) -> bool:
    '''Check if valid start command'''
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'START'


def is_stop(args: List[str]) -> bool:
    '''Check if valid stop command'''
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'STOP'


def is_undo(args: List[str]) -> bool:
    '''Check if valid undo command'''
    return len(args) == 2 and args[1].upper() == 'UNDO'


def is_message(args: List[str]) -> bool:
    '''Check if message supplied with start/stop command'''
    return len(args) == 4 and args[2].upper() == '-M'


def is_all_alpha(name: str) -> bool:
    '''Check if name supplied is only made of letters'''
    return all([char.isalpha() for char in name])


def is_valid(args: List[str]) -> bool:
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
