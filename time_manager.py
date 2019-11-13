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
from lib.constants import PATH_TO_USERS, PATH_TO_STDOUT

if __name__ == "__main__":
    # gets the arguments passed in when run as a script/command
    # (ex. ./time_manager.py NAME START/STOP/UNDO/VIEW [N])
    args = sys.argv[1:]

    os.chdir(PATH_TO_USERS)

    # checks whether to display help or to run the script
    if not is_valid(args) or is_help(args[0]):
        display_help()
    else:
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)

        sys.stdout = open(PATH_TO_STDOUT, 'w')

        run(*args)

        sys.stdout.close()
        sys.stdout = sys.__stdout__

        with open(PATH_TO_STDOUT) as stdout:
            lines = stdout.readlines()
            content = ''.join(lines)
            if len(lines) <= os.get_terminal_size().lines:
                print(content, end='')
            else:
                subprocess.run(['less'], input=content.encode('ascii'))

        os.remove(PATH_TO_STDOUT)
        os.rmdir(tmp_path)
