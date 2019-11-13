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
PATH_TO_USERS = os.environ['HOME'] + '/time_manager/users'
