from datetime import datetime
from typing import Union

from .helpers import readlines, sanitize, last_stop
from .display import print_error
from .constants import FILE_DEST, TIME_FORMAT_PATTERN, MESSAGE_DELIM, EOL


def stop(message: Union[str, None], colored: bool) -> None:
    """Add stop time."""
    if last_stop(readlines()[-1]):
        msg = "Cannot 'stop' twice in a row!"
        print_error(msg) if colored else print(msg)
        return

    if message is None:
        message = ''

    message = sanitize(message)
    with open(FILE_DEST, 'a') as f:
        f.write(f'{datetime.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{EOL}')
