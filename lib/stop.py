from datetime import datetime

from .helpers import readlines, sanitize, last_stop
from .constants import FILE_DEST, TIME_FORMAT_PATTERN, MESSAGE_DELIM, EOL


def stop(message: str) -> None:
    '''Add stop time'''
    if last_stop(readlines()[-1]):
        print("Cannot 'stop' twice in a row!")
        return
    message = sanitize(message)
    with open(FILE_DEST, 'a') as f:
        f.write(f'{datetime.now().strftime(TIME_FORMAT_PATTERN)}'
                f'{MESSAGE_DELIM}{message}{EOL}')
