import os
from typing import List


from .constants import FILE_DEST, DELIMETER, EOL
from .helpers import write, parse_args
from .view import view
from .undo import undo
from .start import start
from .stop import stop


def run(name: str, command: str, args: List[str], flags: List[str]) -> None:
    """Run main program."""
    name = name.upper()
    command = command.upper()

    # checks to see if the directory f'{name}' exists,
    # and if it doesn't it creates the dir
    if not os.path.isdir(name):
        os.mkdir(name)

    os.chdir(name)

    # checks to see if the data file exists,
    # and if it doesn't, it creates the file
    if not os.path.isfile(FILE_DEST):
        write([f'START{DELIMETER}STOP{EOL}'])

    timeframe_from, timeframe_to, message, colored = parse_args(args, flags)

    if command == 'START':
        start(message, colored)
    elif command == 'STOP':
        stop(message, colored)
    elif command == 'UNDO':
        undo(colored)
    elif command == 'VIEW':
        view(timeframe_from, timeframe_to, colored)
