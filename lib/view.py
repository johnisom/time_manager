from datetime import datetime
from typing import Union


from .helpers import (get_split_lines, last_start, get_times,
                     indices_in_timeframe, datetime_range, readlines)
from .display import display, display_lines, display_timeframe
from .constants import TIME_FORMAT_PATTERN


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
