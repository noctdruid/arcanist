# arc-tasks

## about
'arc-tasks' is minimalistic program designed for command-line-interface,
working with asci escape sequences supported terminals, handy with drop-down
terminals, nicely formatted task-objectives right in terminal with
group separation, nice progress/status symbols, terminal-fitting design,
minimal statistics per group, overall statistics, start date, finish date,
archiving multi-group tasks and navigating through archive with UI.

## requirements

- python 3.8+
- pip 22.2+
- xterm-256color (terminal emulator or other that supports ansi)  # need to be added string in src/arc/resolve.py

## installation
```
# PyPi package:
pip install arc-tasks

# add PATH in .bashrc or .zshrc  # your shell configuration file
# and optionally add short alias arc
export PATH="$PATH:$HOME/.local/bin/"
alias arc="arc-tasks"
```

## usage/guide
```
    usage: arc-tasks [OPT]
    for usage examples type: arc-tasks --usage

    -c, --create        create group & task
    -t, --task          add task to the group
    -g, --group         change name of the group
    -e, --edit          edit task description
    -r, --remove        remove task
    -a, --archive       create archive and archive whole group
    -p, --purge         purge whole group and tasks
    -s, --start         change state of task(s) to 'in-progress'
    -f, --finish        change state of task(s) to 'done'

    --board             show tasks board (default)
    --append            add group to existing archive
    --expand            expand task description
    --show              show archived tasks
    --reset             restart program to no task entries
    --help              show this help message
    --usage             show examples of usage
```

```
    program usage examples:

    arc-tasks -c <group_name> <task_desc>
    arc-tasks -t <group_id> <task_desc>
    arc-tasks -g <group_id> <new_group_name>
    arc-tasks -e <group_id> <task_id> <new_task_desc>
    arc-tasks -r <group_id> <task_id>
    arc-tasks -a <group_id> <archive_name>
    arc-tasks -p <group_id>
    arc-tasks -s <group_id> <task_id> <task_id> ...
    arc-tasks -f <group_id> <task_id> <task_id> ...
    arc-tasks --board
    arc-tasks --append <group_id> <archive_name>
    arc-tasks --expand <group_id> <task_id>
    arc-tasks --show
    arc-tasks --reset
    arc-tasks --help
    arc-tasks --usage
```

## license
**GNU General Public License v3**