import os
from typing import List


from .constants import FILE_DEST, DELIMETER, EOL
from .helpers import write
from .view import view
from .undo import undo
from .start import start
from .stop import stop


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
