import os
from typing import List


from .constants import FILE_DEST, DELIMETER, EOL
from .helpers import write, parse_args
from .view import view
from .undo import undo
from .start import start
from .stop import stop


def run(name: str, command: str, *args: List[str]) -> None:
    '''Run main program'''
    name = name.upper()
    command = command.upper()

    # checks to see if the directory f'{name}' exists,
    # and if it doesn't it creates the dir
    if not os.path.isdir(name):
        os.mkdir(name)

    os.chdir(name)

    # checks to see if the data.csv file exists,
    # and if it doesn't, it creates the file
    if not os.path.isfile(FILE_DEST):
        write([f'START{DELIMETER}STOP{EOL}'])

    timeframe_from, timeframe_to, message = parse_args(args)

    if command == 'START':
        start(message)
    elif command == 'STOP':
        stop(message)
    elif command == 'UNDO':
        undo()
    elif command == 'VIEW':
        view(timeframe_from, timeframe_to)
