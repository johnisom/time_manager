import os


SEC_IN_DAY = 86_400
SEC_IN_HOUR = 3_600
SEC_IN_MIN = 60

TIME_FORMAT_PATTERN = '%a %Y-%m-%d %H:%M:%S'

FILE_DEST = 'data.psv'

DELIMETER = '|'
DELIM_REPLACEMENT = '^'
MESSAGE_DELIM = '%%'
EOL = '\n'

FORBIDDEN = [DELIMETER, MESSAGE_DELIM, EOL]

PATH_TO_HELP = os.environ['HOME'] + '/time_manager/help.txt'
PATH_TO_STDOUT = os.environ['HOME'] + '/time_manager/tmp/stdout.txt'
PATH_TO_TMP = os.environ['HOME'] + '/time_manager/tmp'
PATH_TO_USERS = os.environ['HOME'] + '/time_manager/users'


class colors:

    RESET = '\u001b[0m'

    class FG:
        BLK = '\u001b[30m'
        RED = '\u001b[31m'
        GRN = '\u001b[32m'
        YEL = '\u001b[33m'
        BLU = '\u001b[34m'
        MAG = '\u001b[35m'
        CYA = '\u001b[36m'
        WHI = '\u001b[37m'

    class BG:
        BLK = '\u001b[40m'
        RED = '\u001b[41m'
        GRN = '\u001b[42m'
        YEL = '\u001b[43m'
        BLU = '\u001b[44m'
        MAG = '\u001b[45m'
        CYA = '\u001b[46m'
        WHI = '\u001b[47m'
