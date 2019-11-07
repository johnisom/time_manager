# time_manager

## Huge work in progress

I went about writing this without any rhyme or reason,
and you can see that in the source code.
This will need mega refactoring, but so far, stores timestamps in
a csv file when you run the start and stop commands. When you run
the view command, it converts those to nice-to-read date-time formats
and gives you an average of how many hours you studied for the past
N days. Check out help.txt for help.

## Installation

In your home directory, clone this repo into it with a directory name of
`time_manager`. Then, in your `.bashrc` or `.bash_profile`, create an alias
like so: `alias NAME-THAT-YOU-WANT="~/time_manager/time_manager.py"`.
Then after that alias is loaded, you can call the `time_manager` program with
the name of your alias from anywhere.
