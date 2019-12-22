from typing import List

from .constants import (FLAGS, LONG_MESSAGE_FLAG, LONG_NOCOLOR_FLAG,
                        LONG_TIME_FLAG, VIEW_OPTION_FLAGS)


def is_help(arg: str) -> bool:
    """Check if command supplied is a help command."""
    arg = arg.upper()
    return (arg == 'HELP' or
            arg == '-H' or
            arg == '--HELP')


def is_view(args: List[str], flags: List[str]) -> bool:
    """
    Check if valid view command.

    A view command is valid if the command VIEW is supplied, 1-3 arguments
    are supplied, and the (optional) 2nd and 3rd are valid timeframe ranges.

    Examples:
        ['VIEW', 5, 2] are valid arguments for VIEW because they are
        3 long, VIEW is supplied, and 5 days ago to 2 days ago is a valid
        range.

        ['MESSAGE', 5, 2] are invalid arguments because VIEW is not
        supplied.

        ['VIEW'] are valid arguments because they are 1 long and VIEW
        is supplied.

        ['VIEW', 3, 6] are invalid arguments because 3 days ago to 6
        days ago is an invalid range (cannot go backwards).

        ['VIEW', _, 3] are valid arguments only if there are more than
        3 days of history becuase _ will be interpreted as the earliest day on
        record.

    NOTE: only the -nc/--color=false flag can be passed in with this method.
    """
    if len(flags) > 2:
        return False
    if len(flags) == 2 and LONG_NOCOLOR_FLAG not in flags:
        return False
    if len(args) >= 2:
        if not is_valid_from(args[1]):
            return False
    if len(args) == 3:
        if not is_valid_to(args[2], args[1]):
            return False
    return (len(args) >= 1 and len(args) <= 3) and args[0].upper() == 'VIEW'


def is_valid_from(arg: str) -> bool:
    """Check FROM is integer greater than 0 or underscore."""
    try:
        return arg == '_' or int(arg) > 0
    except ValueError:
        return False


def is_valid_to(to_arg: str, from_arg: str) -> bool:
    """Check TO is valid compared to itself and to FROM."""
    try:
        if from_arg == '_':
            from_arg = int(to_arg) + 1
        else:
            from_arg = int(from_arg)
        return int(to_arg) >= 0 and int(to_arg) < from_arg
    except ValueError:
        return False


def is_start(args: List[str], flags: List[str]) -> bool:
    """Check if valid start command."""
    return ((is_message(args, flags) or len(args) == 1) and
            args[0].upper() == 'START')


def is_stop(args: List[str], flags: List[str]) -> bool:
    """Check if valid stop command."""
    return ((is_message(args, flags) or len(args) == 1) and
            args[0].upper() == 'STOP')


def is_undo(args: List[str]) -> bool:
    """Check if valid undo command."""
    return len(args) == 1 and args[0].upper() == 'UNDO'


def is_edit(args: List[str], flags: List[str]) -> bool:
    """Check if valid edit command."""
    if len(flags) > 3:
        return False
    if len(flags) == 3 and (LONG_MESSAGE_FLAG not in flags or
                            LONG_NOCOLOR_FLAG not in flags):
        return False
    if len(args) > 3:
        return False
    return len(args) + len(flags) > 1 and args[0].upper() == 'EDIT'


def is_message(args: List[str], flags: List[str]) -> bool:
    """Check if message is supplied with START/STOP command."""
    return len(args) == 2 and LONG_MESSAGE_FLAG in flags


# TODO: make it so this will accept -4 and +4 mins flags.
def is_good_flags(flags: List[str]) -> bool:
    """Check if all flags are known to program."""
    acceptable = set(FLAGS.values())
    is_plus_minus_mins = any([flag[0:2] != '--'
                              and str(int(flag[1:])) == flag[1:]
                              for flag in flags])
    return acceptable.issuperset(flags) or is_plus_minus_mins


def is_valid(args: List[str], flags: List[str]) -> bool:
    """Check if format of arguments is correct as specified in help.txt."""
    is_good_commands = (is_start(args, flags) or is_stop(args, flags) or
                        is_view(args, flags) or is_undo(args) or
                        is_edit(args, flags))
    return is_good_commands and is_good_flags(flags)
