from typing import List, Optional


def display_lines(lines: List[List[List[str]]],
                  times: List[List[datetime]]) -> None:
    '''Display start times, stop times, messages, and session times'''
    for idx, (start, stop) in enumerate(lines):
        start_message = start[1]
        stop_message = stop[1]
        if start_message:
            start_message = f' -> "{start_message}"'
        if stop_message:
            stop_message = f' -> "{stop_message}"'

        print(f'Start: {start[0]}{start_message}')
        print(f'Stop: {stop[0]}{stop_message}')
        delta = times[idx][1] - times[idx][0]
        display('Session time', delta.seconds, '\n')


def display(title: str, total_seconds: int,
            trailer: Optional[str] = '') -> None:
    '''Display line of time'''
    secs = total_seconds % SEC_IN_MIN
    mins = total_seconds // SEC_IN_MIN % SEC_IN_MIN
    hours = total_seconds // SEC_IN_HOUR % SEC_IN_MIN
    print(f'{title}: {hours:02}:{mins:02}:{secs:02}{trailer}')


def display_timeframe(timeframe_from: int, timeframe_to: int) -> None:
    '''Display info about timeframe'''
    if timeframe_to == 0:
        print(f'\nShowing results for the past {timeframe_from} day(s)\n')
    else:
        print(f'\nShowing results from {timeframe_from}', end=' ')
        print(f'days ago to {timeframe_to} day(s) ago\n')


def display_help() -> None:
    '''Output help.txt to the console'''
    with open('help.txt') as f:
        print(f.read())
