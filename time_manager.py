#!/usr/bin/python3

# Update the above shebang if that path does not
# exist on your system. Make sure that it points
# to a version of python 3.6 or greater.

import sys
import os
from datetime import datetime, timedelta


# from modules as part of project
from command_validation import *
from display import display_help
from constants import FILE_DEST, DELIMETER, EOL
from view import view
from undo import undo
from start import start
from stop import stop

os.chdir(os.environ['HOME'] + '/time_manager')


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


if __name__ == "__main__":
    # gets the arguments passed in when run as a script/command
    # (ex. ./time_manager.py NAME START/STOP/UNDO/VIEW [N])
    args = sys.argv[1:]

    # checks whether to display help or to run the script
    if not is_valid(args) or is_help(args[0]):
        display_help()
    else:
        run(*args)
