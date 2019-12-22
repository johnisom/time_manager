from datetime import datetime
from typing import Union

from .helpers import last_start, sanitize, readlines
from .display import print_error
from .constants import FILE_DEST, TIME_FORMAT_PATTERN, MESSAGE_DELIM, DELIMETER


def start(message: Union[str, None], colored: bool) -> None:
    """Add start time."""
    if last_start(readlines()[-1]):
        msg = "Cannot 'start' twice in a row!"
        print_error(msg) if colored else print(msg)
        return

    if message is None:
        message = ''

    message = sanitize(message)
    with open(FILE_DEST, 'a') as f:
        f.write(f'{datetime.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{DELIMETER}')
