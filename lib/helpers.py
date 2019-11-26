from datetime import datetime, timedelta
from typing import List, Union, Tuple
import os
import subprocess


from .constants import (FORBIDDEN, FILE_DEST, EOL, DELIMETER, FLAGS,
                        MESSAGE_DELIM, DELIM_REPLACEMENT, PATH_TO_STDOUT,
                        TIME_FORMAT_PATTERN, LONG_NOCOLOR_FLAG,
                        LONG_MESSAGE_FLAG)


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


def parse_args(args: List[str], flags: List[str]) -> Tuple[Union[str, None]]:
    """Parse/split a list of arguments into their components."""
    timeframe_from = None
    timeframe_to = None
    message = ''
    colored = True
    view_option = "default"

    if LONG_NOCOLOR_FLAG in flags:
        colored = False

    if len(args) == 1 and LONG_MESSAGE_FLAG in flags:
        message = args[0]
    elif len(args) == 1 and LONG_MESSAGE_FLAG not in flags:
        timeframe_from = args[0]
    elif len(args) == 2:
        timeframe_from = args[0]
        timeframe_to = args[1]

    if flags and LONG_NOCOLOR_FLAG not in flags:
        view_option = flags[0].strip('-')
    elif len(flags) > 1 and LONG_NOCOLOR_FLAG in flags:
        view_option = flags[flags.index(LONG_NOCOLOR_FLAG) - 1].strip('-')

    return timeframe_from, timeframe_to, message, view_option, colored


def output_everything() -> None:
    """Output all standard output to stdout or less."""
    with open(PATH_TO_STDOUT) as stdout:
        lines = stdout.readlines()
        less_content = '\n  ' + '  '.join(lines)
        content = ''.join(lines)
        if len(lines) <= os.get_terminal_size().lines:
            print(content, end='')
        else:
            subprocess.run(['less', '-RX'], input=less_content.encode('utf-8'))


def convert_timeframes(timeframe_from: Union[str, None],
                       timeframe_to: Union[str, None],
                       times: List[List[datetime]]) -> Tuple[int]:
    """Convert timeframes from str or None into integers."""
    if timeframe_from is None or timeframe_from == '_':
        last_date = times[-1][0].date()
        first_date = times[0][1].date()
        timeframe_from = (last_date - first_date).days + 1
    else:
        timeframe_from = int(timeframe_from)

    timeframe_to = 0 if timeframe_to is None else int(timeframe_to)

    return timeframe_from, timeframe_to


def separate_args_and_flags(sys_args: List[str]) -> Tuple[List[str]]:
    """Separate regular arguments and flag arguments into separate lists."""
    args = []
    flags = []
    for sys_arg in sys_args:
        if sys_arg.startswith('--'):
            flags.append(sys_arg)
        elif sys_arg.startswith('-'):
            flags.append(FLAGS.get(sys_arg))
        else:
            args.append(sys_arg)

    return args, flags
