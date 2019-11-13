from typing import List


def is_help(arg: str) -> bool:
    """Check if command supplied is a help command."""
    arg = arg.upper()
    return (arg == 'HELP' or
            arg == '-H' or
            arg == '--HELP')


def is_view(args: List[str]) -> bool:
    """
    Check if valid view command.

    A view command is valid if the command VIEW is supplied, 2-4 arguments
    are supplied, and the (optional) 3rd and 4th are valid timeframe ranges.

    Examples:
        ['NAME', 'VIEW', 5, 2] are valid arguments for VIEW because they are
        4 long, VIEW is supplied, and 5 days ago to 2 days ago is a valid
        range.

        ['NAME', 'MESSAGE', 5, 2] are invalid arguments because VIEW is not
        supplied.

        ['NAME', 'VIEW'] are valid arguments because they are 2 long and VIEW
        is supplied.

        ['NAME', 'VIEW', 3, 6] are invalid arguments because 3 days ago to 6
        days ago is an invalid range (cannot go backwards).

        ['NAME', 'VIEW', _, 3] are valid arguments only if there are more than
        3 days of history becuase _ will be interpreted as the earliest day on
        record.
    """
    if len(args) >= 3:
        if not is_valid_from(args[2]):
            return False
    if len(args) == 4:
        if not is_valid_to(args[3], args[2]):
            return False
    return (len(args) >= 2 and len(args) <= 4) and args[1].upper() == 'VIEW'


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


def is_start(args: List[str]) -> bool:
    """Check if valid start command."""
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'START'


def is_stop(args: List[str]) -> bool:
    """Check if valid stop command."""
    return (is_message(args) or len(args) == 2) and args[1].upper() == 'STOP'


def is_undo(args: List[str]) -> bool:
    """Check if valid undo command."""
    return len(args) == 2 and args[1].upper() == 'UNDO'


def is_message(args: List[str]) -> bool:
    """Check if message is supplied with START/STOP command."""
    try:
        flag = args[2].lower()
    except IndexError:
        return False

    return len(args) == 4 and flag == '-m' or flag == '--message'


def is_all_alpha(name: str) -> bool:
    """Check if name supplied is only made of letters."""
    return all([char.isalpha() for char in name])


def is_valid(args: List[str]) -> bool:
    """Check if format of arguments is correct as specified in help.txt."""
    return (is_start(args) or is_stop(args) or
            is_view(args) or is_undo(args)) and is_all_alpha(args[0])
