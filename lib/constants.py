import os


SEC_IN_DAY = 86_400
SEC_IN_HOUR = 3_600
SEC_IN_MIN = 60

TIME_FORMAT_PATTERN = '%a %Y-%m-%d %H:%M:%S'
DATE_FORMAT_PATTERN = '%a %Y-%m-%d'

FILE_DEST = 'data.psv'

DELIMETER = '|'
DELIM_REPLACEMENT = '^'
MESSAGE_DELIM = '%%'
EOL = '\n'

FORBIDDEN = [DELIMETER, MESSAGE_DELIM, EOL]

PATH_TO_HELP = os.environ['HOME'] + '/time_manager/HELP.txt'
PATH_TO_STDOUT = os.environ['HOME'] + '/time_manager/tmp/stdout.txt'
PATH_TO_TMP = os.environ['HOME'] + '/time_manager/tmp'
PATH_TO_DATA = os.environ['HOME'] + '/time_manager/data'

SHORT_MESSAGE_FLAG = '-m'
LONG_MESSAGE_FLAG = '--message'

SHORT_NOCOLOR_FLAG = '-nc'
LONG_NOCOLOR_FLAG = '--nocolor'

SHORT_TIME_FLAG = '-t'
LONG_TIME_FLAG = '--time'

SHORT_DAILY_DIGEST_FLAG = '-d'
LONG_DAILY_DIGEST_FLAG = '--daily-digest'

SHORT_DAY_DELIMITED_FLAG = '-dd'
LONG_DAY_DELIMITED_FLAG = '--day-delimited'

SHORT_WEEKLY_DIGEST_FLAG = '-w'
LONG_WEEKLY_DIGEST_FLAG = '--weekly-digest'

SHORT_WEEK_DELIMITED_FLAG = '-wd'
LONG_WEEK_DELIMITED_FLAG = '--week-delimited'

FLAGS = {
    SHORT_MESSAGE_FLAG: LONG_MESSAGE_FLAG,
    SHORT_NOCOLOR_FLAG: LONG_NOCOLOR_FLAG,
    SHORT_TIME_FLAG: LONG_TIME_FLAG,
    SHORT_DAILY_DIGEST_FLAG: LONG_DAILY_DIGEST_FLAG,
    SHORT_DAY_DELIMITED_FLAG: LONG_DAY_DELIMITED_FLAG,
    SHORT_WEEKLY_DIGEST_FLAG: LONG_WEEKLY_DIGEST_FLAG,
    SHORT_WEEK_DELIMITED_FLAG: LONG_WEEK_DELIMITED_FLAG
}


class colors:

    RESET = '\x1b[0m'

    class FG:
        BLK = '\x1b[30m'
        RED = '\x1b[31m'
        GRN = '\x1b[32m'
        YEL = '\x1b[33m'
        BLU = '\x1b[34m'
        MAG = '\x1b[35m'
        CYA = '\x1b[36m'
        WHI = '\x1b[37m'

        class BRIGHT:
            BLK = '\x1b[30;1m'
            RED = '\x1b[31;1m'
            GRN = '\x1b[32;1m'
            YEL = '\x1b[33;1m'
            BLU = '\x1b[34;1m'
            MAG = '\x1b[35;1m'
            CYA = '\x1b[36;1m'
            WHI = '\x1b[37;1m'

    class BG:
        BLK = '\x1b[40m'
        RED = '\x1b[41m'
        GRN = '\x1b[42m'
        YEL = '\x1b[43m'
        BLU = '\x1b[44m'
        MAG = '\x1b[45m'
        CYA = '\x1b[46m'
        WHI = '\x1b[47m'
