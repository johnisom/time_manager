from datetime import datetime, timedelta
from typing import List, Union, Tuple
import os
import subprocess


from .constants import (FORBIDDEN, DELIM_REPLACEMENT, EOL,
                        DELIMETER, MESSAGE_DELIM, FILE_DEST,
                        TIME_FORMAT_PATTERN, PATH_TO_STDOUT)


def sanitize(text: str) -> str:
    """Replace forbidden character sequences."""
    for forbidden in FORBIDDEN:
        text = text.replace(forbidden, DELIM_REPLACEMENT)
    return text


def get_split_lines() -> List[List[List[str]]]:
    """Get lines split into entry and message subcomponents."""
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
    """From split lines create sublists of start and stop datetime objects."""
    # [[datetime, datetime], [datetime, datetime], etc.]
    times = []
    for start, stop in lines:
        start = to_datetime(start[0])
        stop = to_datetime(stop[0])
        times.append([start, stop])
    return times


def indices_in_timeframe(times: List[List[datetime]], datetime_from: datetime,
                         datetime_to: datetime) -> int:
    """Find indices that selects times from timeframe_from to timeframe_to."""
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
    """Get the timeframe as 2 datetimes."""
    today = datetime.now().date()

    from_days_ago = today - timedelta(days=int(timeframe_from) - 1)
    to_days_ago = today - timedelta(days=int(timeframe_to))

    from_days_ago_datetime = datetime(from_days_ago.year,
                                      from_days_ago.month, from_days_ago.day)
    to_days_ago_datetime = datetime(to_days_ago.year, to_days_ago.month,
                                    to_days_ago.day, 23, 59, 59)
    return from_days_ago_datetime, to_days_ago_datetime


def to_datetime(string: str) -> datetime:
    """Convert str to datetime."""
    return datetime.strptime(string, TIME_FORMAT_PATTERN)


def readlines() -> List[str]:
    """Get data from data storage."""
    with open(FILE_DEST) as f:
        return f.readlines()


def write(lines: List[str]) -> None:
    """Write data to data storage."""
    with open(FILE_DEST, 'w') as f:
        for line in lines:
            f.write(line)


def last_stop(line: str) -> bool:
    """Determine if last time added to line was a stop time."""
    return line[-1] == EOL


def last_start(line: str) -> bool:
    """Determine if last time added to line was a start time."""
    return line[-1] == DELIMETER


def parse_args(args: List[str]) -> Tuple[Union[str, None]]:
    """Parse/split a list of arguments into their components."""
    timeframe_from = None
    timeframe_to = None
    message = ''

    if len(args) == 1:
        timeframe_from = args[0]
    elif len(args) == 2:
        if args[0] == '-m' or args[0] == '--message':
            message = args[1]
        else:
            timeframe_from = args[0]
            timeframe_to = args[1]

    return timeframe_from, timeframe_to, message


def output_everything() -> None:
    """Output all standard output to stdout or less."""
    with open(PATH_TO_STDOUT) as stdout:
        lines = stdout.readlines()
        less_content = '\n  ' + '  '.join(lines)
        content = ''.join(lines)
        if len(lines) <= os.get_terminal_size().lines:
            print(content, end='')
        else:
            subprocess.run(['less'], input=less_content.encode('ascii'))


def convert_timeframes(timeframe_from: Union[str, None],
                       timeframe_to: Union[str, None],
                       times: List[List[datetime]]) -> Tuple[int]:
    """Convert timeframes from str or None into integers."""
    if timeframe_from is None or timeframe_from == '_':
        timeframe_from = (times[-1][0] - times[0][0]).days + 1
    else:
        timeframe_from = int(timeframe_from)

    timeframe_to = 0 if timeframe_to is None else int(timeframe_to)

    return timeframe_from, timeframe_to
