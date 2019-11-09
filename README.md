# time_manager

## Huge work in progress

I went about writing this without any rhyme or reason,
and you can see that in the source code.
This will need mega refactoring, but so far, stores timestamps in
a psv file when you run the start and stop commands. When you run
the view command, it converts those to nice-to-read date-time formats
and gives you an average of how many hours you studied for the past
N days.
I am glad to say that I have done some major work and refactoring on this,
so it is much better to work with.
__Check out help.txt for help.__

## Installation

In your home directory, clone this repo into it like so:

```bash
cd ~
git clone https://github.com/johnisom/time_manager.git
```

Then, in your `~/.bashrc` or `~/.bash_profile`, create an alias
like so:

```bash
alias time_manager="~/time_manager/time_manager.py"
```

This is also acceptable:

```bash
alias tm="~/time_manager/time_manager.py"
```

Then after that alias is loaded (ex. `$ source ~/.bashrc`), you can call the
`time_manager` program from anywhere.

### Dependencies

This relies on python 3.6 or greater (uses f-strings), so make sure you have that installed.
Also, if you dont have the path `/usr/bin/python3`, update the shebang at the top of
`~/time_manager/time_manager.py` from `#!/usr/bin/python3` to `#!/your/path/to/python/3.6/or/greater`.

## TODOS

* ~~Allow `VIEW` if currently in session. Will probably say 'Currently: ' instead
  of 'Stopped: ' and show timestamp with no message.~~
  Now says `Stop: [timestamp] -> "CURRENT"`
* ~~Add docstrings to all functions without them~~
* Create longer, better, and more descriptive docstrings for all functions
* ~~Clean up all functions~~
* Create a config function -- consult Adam for more info
* Refactor the crap out of everything~~ -- needs a total rewrite nearly from scratch~~
* Add more view options such as viewing average hours per week, etc
* Add a GUI or GUI-looking thing when printing out to console
* ~~__Add functionality to add messages to a `START` or `STOP` command__
  Look at updated `help.txt` for info on how to use it. Still needs to be implemented
  in code.~~
* Add categories of what your time is going to, like coding, working out,
  reading, etc.
* ~~Add typing~~
