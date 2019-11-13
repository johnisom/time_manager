from datetime import datetime
from typing import Union


from .helpers import (get_split_lines, last_start, get_times,
                      indices_in_timeframe, datetime_range, readlines,
                      convert_timeframes)
from .display import (display_summary, display_lines, display_timeframe,
                      display_help)
from .constants import TIME_FORMAT_PATTERN


def view(timeframe_from: Union[str, None],
         timeframe_to: Union[str, None]) -> None:
    """Output data and summaries for logged time."""
    lines = get_split_lines()

    # Use current time as end time if no end time
    if last_start(readlines()[-1]):
        now_formatted = datetime.now().strftime(TIME_FORMAT_PATTERN)
        lines[-1][1] = [now_formatted, 'CURRENT']

    times = get_times(lines)
    if not times:
        print('No data to report')
        return

    timeframes = convert_timeframes(timeframe_from, timeframe_to, times)
    timeframe_from, timeframe_to = timeframes

    if timeframe_from <= timeframe_to:
        display_help()
        return

    idx_from, idx_to = indices_in_timeframe(
        times, *datetime_range(timeframe_from, timeframe_to))
    lines = lines[idx_from:idx_to]
    times = times[idx_from:idx_to]

    diff_seconds = [(stop - start).seconds for start, stop in times]
    total_total_seconds = sum(diff_seconds)
    avg_total_seconds = total_total_seconds // (timeframe_from - timeframe_to)

    display_timeframe(timeframe_from, timeframe_to)
    display_lines(lines, times)
    display_summary('Average', avg_total_seconds, ' per day')
    display_summary('Total', total_total_seconds)
