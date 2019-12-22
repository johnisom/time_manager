from typing import List, Optional
from datetime import datetime
import os
import sys

from .constants import SEC_IN_MIN, SEC_IN_HOUR, PATH_TO_HELP, colors


def display_lines(lines: List[List[List[str]]],
                  times: List[List[datetime]], colored: bool) -> None:
    """
    Display start times, stop times, messages, and session times.

    Follows this format:
        Start: timestamp( -> "message")
        Stop: timestamp( -> "message")
        Session time: hour:min:sec
    """
    for (start_time, stop_time),\
            ((start_str, start_message),
             (stop_str, stop_message)) in zip(times, lines):
        if start_message:
            start_message = f'-> {start_message}'
        if stop_message:
            stop_message = f'-> {stop_message}'

        display_line('Start', start_str, start_message, colored)
        display_line('Stop', stop_str, stop_message, colored)

        delta = stop_time - start_time
        display_summary('Session time', delta.seconds, colored, '\n')


def display_line(title: str, time: str, message: str, colored: bool) -> None:
    """Help display_lines by displaying just one line."""
    if colored:
        print(f'{colors.FG.MAG}{title}: {colors.FG.BRIGHT.GRN}{time} '
              f'{colors.FG.BRIGHT.CYA}{message}'
              f'{colors.RESET}')
    else:
        print(f'{title}: {time} {message}')


def display_summary(title: str, total_seconds: int, colored: bool,
                    trailer: Optional[str] = '') -> None:
    """Display line of time."""
    secs = total_seconds % SEC_IN_MIN
    mins = total_seconds // SEC_IN_MIN % SEC_IN_MIN
    hours = total_seconds // SEC_IN_HOUR
    if colored:
        print(f'{colors.FG.GRN}{title}: {colors.FG.YEL}{hours:02}:{mins:02}:'
              f'{secs:02}{colors.RESET}{trailer}')
    else:
        print(f'{title}: {hours:02}:{mins:02}:{secs:02}{trailer}')


def display_timeframe(timeframe_from: int, timeframe_to: int,
                      colored: bool) -> None:
    """Display info about range of timeframe."""
    if timeframe_to == 0:
        if colored:
            print('\nShowing results for the past '
                  f'{colors.FG.BLU}{timeframe_from}{colors.RESET} day(s)\n')
        else:
            print(f'\nShowing results for the past {timeframe_from} day(s)\n')
    else:
        if colored:
            print(f'\nShowing results from {colors.FG.BLU}{timeframe_from}'
                  f'{colors.RESET} days ago to {colors.FG.BLU}'
                  f'{timeframe_to}{colors.RESET} day(s) ago\n')
        else:
            print(f'\nShowing results from {timeframe_from} '
                  f'days ago to {timeframe_to} day(s) ago\n')


def display_help() -> None:
    """Output help.txt to the console."""
    with open(PATH_TO_HELP) as f:
        print(f.read())


def print_error(msg: str) -> None:
    """Print message as an error."""
    print(f'{colors.FG.RED}{msg}{colors.RESET}', file=sys.stderr)
