from helpers import readlines, write, last_stop
from constants import DELIMETER


def undo() -> None:
    '''Delete last start/stop time added'''
    lines = readlines()
    if len(lines) == 1:
        print("Cannot 'undo' anymore, reached max undo!")
        return
    data = lines[:-1]
    last_line = lines[-1]

    if last_stop(last_line):
        data.append(last_line.split(DELIMETER)[0] + DELIMETER)

    # rewrite data.csv with all the previous data
    # except the last start/stop time
    write(data)
