import os
from typing import List


from .constants import FILE_DEST, DELIMETER, EOL
from .helpers import (write, parse_args, parse_start_stop_args,
                      parse_undo_args, parse_edit_args, parse_view_args)
from .view import view
from .undo import undo
from .start import start
from .stop import stop
from .edit import edit


def run(command: str, args: List[str], flags: List[str]) -> None:
    """Run main program."""
    command = command.upper()

    # checks to see if the data file exists,
    # and if it doesn't, it creates the file
    if not os.path.isfile(FILE_DEST):
        write([f'START{DELIMETER}STOP{EOL}'])

    # timeframe_from, timeframe_to, message,
    # view_option, colored, time, mins = parse_args(args, flags)

    if command == 'START':
        # start(message, colored)
        start(*parse_start_stop_args(args, flags))
    elif command == 'STOP':
        # stop(message, colored)
        stop(*parse_start_stop_args(args, flags))
    elif command == 'UNDO':
        # undo(colored)
        undo(*parse_undo_args(args, flags))
    elif command == 'EDIT':
        edit(*parse_edit_args(args, flags))
    elif command == 'VIEW':
        # view(timeframe_from, timeframe_to, view_option, colored)
        view(*parse_view_args(args, flags))
