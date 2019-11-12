#!/usr/bin/python3

# Update the above shebang if that path does not
# exist on your system. Make sure that it points
# to a version of python 3.6 or greater.

import sys
import subprocess
import os

from lib.run import run
from lib.display import display_help
from lib.command_validation import is_valid, is_help
from lib.constants import PATH_TO_USERS

if __name__ == "__main__":
    # gets the arguments passed in when run as a script/command
    # (ex. ./time_manager.py NAME START/STOP/UNDO/VIEW [N])
    args = sys.argv[1:]

    os.chdir(PATH_TO_USERS)

    # checks whether to display help or to run the script
    if not is_valid(args) or is_help(args[0]):
        display_help()
    else:
        tmp_path = os.environ['HOME'] + '/time_manager/tmp'
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)
        sys.stdout = open(tmp_path + '/stdout.txt', 'w')
        run(*args)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        with open(tmp_path + '/stdout.txt') as stdout:
            lines = stdout.readlines()
            if len(lines) <= os.get_terminal_size().lines:
                for line in lines:
                    print(line, end='')
            else:
                subprocess.run(['less'], input=''.join(lines).encode('ascii'))
        os.remove(tmp_path + '/stdout.txt')
        os.rmdir(tmp_path)
