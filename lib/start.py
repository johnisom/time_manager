from datetime import datetime

from .helpers import last_start, sanitize, readlines
from .constants import FILE_DEST, TIME_FORMAT_PATTERN, MESSAGE_DELIM, DELIMETER


def start(message: str) -> None:
    """Add start time."""
    if last_start(readlines()[-1]):
        print("Cannot 'start' twice in a row!")
        return
    message = sanitize(message)
    with open(FILE_DEST, 'a') as f:
        f.write(f'{datetime.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{DELIMETER}')
