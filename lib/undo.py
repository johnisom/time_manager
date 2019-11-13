from .helpers import readlines, write, last_stop
from .constants import DELIMETER


def undo() -> None:
    """Delete last start/stop time added."""
    lines = readlines()
    if len(lines) == 1:
        print("Cannot 'undo' anymore, reached max undo!")
        return

    data = lines[:-1]
    last_line = lines[-1]
    if last_stop(last_line):
        data.append(last_line.split(DELIMETER)[0] + DELIMETER)

    write(data)  # rewrite data file with all previous data except last entry
