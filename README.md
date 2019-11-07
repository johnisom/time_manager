# time_manager

## Huge work in progress

I went about writing this without any rhyme or reason,
and you can see that in the source code.
This will need mega refactoring, but so far, stores timestamps in
a csv file when you run the start and stop commands. When you run
the view command, it converts those to nice-to-read date-time formats
and gives you an average of how many hours you studied for the past
N days.
Check out help.txt for help.

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

Then after that alias is loaded (ex. `$ source ~/.bashrc`), you can call the
`time_manager` program from anywhere.
