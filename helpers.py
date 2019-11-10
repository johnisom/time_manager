from datetime import datetime, timedelta
from typing import List


from constants import (FORBIDDEN, DELIM_REPLACEMENT, EOL,
                       DELIMETER, MESSAGE_DELIM, FILE_DEST,
                       TIME_FORMAT_PATTERN)


def sanitize(text: str) -> str:
    '''Replace forbidden character sequences'''
    for forbidden in FORBIDDEN:
        text = text.replace(forbidden, DELIM_REPLACEMENT)
    return text


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
