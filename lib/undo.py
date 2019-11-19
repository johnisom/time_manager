from .helpers import readlines, write, last_stop
from .display import print_error
from .constants import DELIMETER


def undo(colored: bool) -> None:
    """Delete last start/stop time added."""
    lines = readlines()
    if len(lines) == 1:
        msg = "Cannot 'undo' anymore, reached max undo!"
        print_error(msg) if colored else print(msg)
        return

    data = lines[:-1]
    last_line = lines[-1]
    if last_stop(last_line):
        data.append(last_line.split(DELIMETER)[0] + DELIMETER)

    write(data)  # rewrite data file with all previous data except last entry
