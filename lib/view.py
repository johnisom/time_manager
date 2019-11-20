from datetime import datetime
from typing import Union, List
import os


from .helpers import (get_split_lines, last_start, get_times,
                      indices_in_timeframe, datetime_range, readlines,
                      convert_timeframes)
from .display import (display_summary, display_lines, display_timeframe,
                      display_help, display_line, print_error)
from .constants import (TIME_FORMAT_PATTERN, DATE_FORMAT_PATTERN, SEC_IN_MIN,
                        SEC_IN_HOUR, colors)


def view(timeframe_from: Union[str, None], timeframe_to: Union[str, None],
         view_option: str, colored: bool) -> None:
    """Output data and summaries for logged time."""
    lines = get_split_lines()

    # Use current time as end time if no end time
    if last_start(readlines()[-1]):
        now_formatted = datetime.now().strftime(TIME_FORMAT_PATTERN)
        lines[-1][1] = [now_formatted, 'CURRENT']

    times = get_times(lines)
    if not times:
        msg = 'No data to report'
        print_error(msg) if colored else print(msg)
        return

    timeframe_from, timeframe_to = convert_timeframes(
        timeframe_from, timeframe_to, times)

    if timeframe_from <= timeframe_to:
        display_help()
        return

    idx_from, idx_to = indices_in_timeframe(
        times, *datetime_range(timeframe_from, timeframe_to))
    lines = lines[idx_from:idx_to]
    times = times[idx_from:idx_to]

    display_timeframe(timeframe_from, timeframe_to, colored)

    args = timeframe_from, timeframe_to, lines, times, colored
    if view_option == 'default':
        default(*args)
    elif view_option == 'daily-digest':
        daily_digest(*args)
    elif view_option == 'day-delimited':
        day_delimited(*args)
    print(view_option)


def default(timeframe_from: int, timeframe_to: int,
            lines: List[List[List[str]]], times: List[List[datetime]],
            colored: bool) -> None:
    """Carry on duties of default view option."""
    diff_seconds = [(stop - start).seconds for start, stop in times]
    total_total_seconds = sum(diff_seconds)
    avg_total_seconds = total_total_seconds // (timeframe_from - timeframe_to)

    if colored:
        print(f'Chosen display: {colors.FG.BRIGHT.RED}DEFAULT{colors.RESET}\n')
    else:
        print('Chosen display: DEFAULT\n')

    display_lines(lines, times, colored)
    display_summary('Average', avg_total_seconds, colored, ' per day')
    display_summary('Total', total_total_seconds, colored)


def daily_digest(timeframe_from: int, timeframe_to: int,
                 lines: List[List[List[str]]], times: List[List[datetime]],
                 colored: bool) -> None:
    """Carry on duties of daily-digest view option as stated in help.txt."""
    daily_times = [0 for _ in range(timeframe_from - timeframe_to)]
    dates = [times[0][1]]
    beg_date = times[0][0].date()
    day = 0
    for start, stop in times:
        if (stop.date() - beg_date).days != day:
            dates.append(stop)
            day += 1
        daily_times[day] += (stop - start).seconds

    total_seconds = sum(daily_times)
    average_seconds = total_seconds // (timeframe_from - timeframe_to)

    if colored:
        print(f'Chosen display: {colors.FG.BRIGHT.RED}DAILY DIGEST'
              f'{colors.RESET}\n')
    else:
        print('Chosen display: DAILY DIGEST\n')

    for date, daily_time in zip(dates, daily_times):
        date = date.strftime(DATE_FORMAT_PATTERN)
        display_summary(date, daily_time, colored)
        print()

    display_summary('\nAverage', average_seconds, colored, ' per day')
    display_summary('Total', total_seconds, colored)


def day_delimited(timeframe_from: int, timeframe_to: int,
                  lines: List[List[List[str]]], times: List[List[datetime]],
                  colored: bool) -> None:
    """Carry on duties of day-delimited view option as stated in help.txt."""
    diff_seconds = [(stop - start).seconds for start, stop in times]
    total_total_seconds = sum(diff_seconds)
    avg_total_seconds = total_total_seconds // (timeframe_from - timeframe_to)

    day_times = [[] for _ in range(timeframe_from - timeframe_to)]
    day_lines = [[] for _ in range(len(day_times))]
    beg_date = times[0][0].date()
    day = 0
    for time, line in zip(times, lines):
        if (time[1].date() - beg_date).days != day:
            day += 1
        day_times[day].append(time)
        day_lines[day].append(line)

    daily_totals = [sum([(stop - start).seconds for start, stop in times])
                    for times in day_times]

    if colored:
        print(f'Chosen display: {colors.FG.BRIGHT.RED}'
              f'DAY DELIMITED{colors.RESET}\n')
    else:
        print('Chosen display: DAY DELIMITED\n')

    for total, times, lines in zip(daily_totals, day_times, day_lines):
        display_lines(lines, times, colored)

        cols = os.get_terminal_size().columns
        if colored:
            print(f'{colors.FG.BRIGHT.MAG}{"=" * (cols - 6)}{colors.RESET}\n')
            display_summary('Daily amount', total, True)
            print(f'\n{colors.FG.BRIGHT.MAG}{"=" * (cols - 6)}'
                  f'{colors.RESET}\n\n')
        else:
            print(f'{"=" * (cols - 6)}\n')
            display_summary('Daily amount', total, False)
            print(f'\n{"=" * (cols - 6)}\n\n')

    display_summary('Average', avg_total_seconds, colored, ' per day')
    display_summary('Total', total_total_seconds, colored)
