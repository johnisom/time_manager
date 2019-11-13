#!/usr/bin/python3

"""
A simple CLI time manager application.

See help.txt and README.md for more info.
"""

# NOTE:
# Update the above shebang if that path does not
# exist on your system. Make sure that it points
# to a version of python 3.6 or greater.

import sys
import os

from lib.run import run
from lib.display import display_help
from lib.command_validation import is_valid, is_help
from lib.helpers import output_everything
from lib.constants import PATH_TO_USERS, PATH_TO_STDOUT, PATH_TO_TMP

if __name__ == "__main__":
    args = sys.argv[1:]

    os.chdir(PATH_TO_USERS)

    if not os.path.isdir(PATH_TO_TMP):
        os.mkdir(PATH_TO_TMP)

    sys.stdout = open(PATH_TO_STDOUT, 'w')

    # checks whether to display help or to run the script
    display_help() if not is_valid(args) or is_help(args[0]) else run(*args)

    sys.stdout.close()
    sys.stdout = sys.__stdout__

    output_everything()

    os.remove(PATH_TO_STDOUT)
    os.rmdir(PATH_TO_TMP)
