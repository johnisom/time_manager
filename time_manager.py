#!/usr/bin/env python3

"""
A simple CLI time manager application.

See help.txt and README.md for more info.
"""

import sys
import os

from lib.run import run
from lib.display import display_help
from lib.command_validation import is_valid, is_help
from lib.helpers import output_everything, separate_args_and_flags
from lib.constants import PATH_TO_DATA, PATH_TO_STDOUT, PATH_TO_TMP

if __name__ == "__main__":
    args, flags = separate_args_and_flags(sys.argv[1:])

    if not os.path.isdir(PATH_TO_DATA):
        os.mkdir(PATH_TO_DATA)

    if not os.path.isdir(PATH_TO_TMP):
        os.mkdir(PATH_TO_TMP)

    os.chdir(PATH_TO_DATA)

    sys.stdout = open(PATH_TO_STDOUT, 'w')

    # checks whether to display help or to run the script
    if not is_valid(args, flags) or is_help(args[0]):
        display_help()
    else:
        run(args[0], args[1:], flags)

    sys.stdout.close()
    sys.stdout = sys.__stdout__

    output_everything()

    os.remove(PATH_TO_STDOUT)
    os.rmdir(PATH_TO_TMP)
