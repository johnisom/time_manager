from datetime import datetime, timedelta
from typing import Union


from .helpers import readlines, write, last_stop, last_start, sanitize
from .display import print_error
from .constants import DELIMETER, MESSAGE_DELIM, TIME_FORMAT_PATTERN, EOL


def edit(message: Union[str, None], time: Union[str, None],
         mins: Union[str, None], colored: bool) -> None:
    """Edit last start/stop time added."""
    lines = readlines()
    if len(lines) == 1:
        msg = "Cannot 'edit' nonexistent data!"
        print_error(msg) if colored else print(msg)
        return
    last_line = lines[-1]

    start, stop = last_line.strip(EOL).split(DELIMETER)
    if last_stop(last_line):
        old_datetime_str, old_message = stop.split(MESSAGE_DELIM)
    elif last_start(last_line):
        old_datetime_str, old_message = start.split(MESSAGE_DELIM)

    if message is not None:
        old_message = sanitize(message)
    if time is not None:
        now = datetime.now()
        hour, min, sec = [int(part) for part in time.split(':')]
        old_datetime_str = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=min, second=sec).strftime(TIME_FORMAT_PATTERN)
    elif mins is not None:
        old_datetime = datetime.strptime(old_datetime_str, TIME_FORMAT_PATTERN)
        new_datetime = old_datetime + timedelta(minutes=int(mins))
        old_datetime_str = new_datetime.strftime(TIME_FORMAT_PATTERN)

    entry = old_datetime_str + MESSAGE_DELIM + old_message

    if last_stop(last_line):
        lines[-1] = start + DELIMETER + entry + EOL
    elif last_start(last_line):
        lines[-1] = entry + DELIMETER

    write(lines)
