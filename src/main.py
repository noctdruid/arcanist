"""
< program name: arc-tasks >
< python version: 3.9.2 >
< author: Predrag Bunic >
< contact: pbunic@proton.me >
< license: GPL v3 >

v1.0.2
'Arc-tasks' is minimalistic program designed for command-line-interface,
working with asci escape sequences supported terminals, handy with drop-down
terminals, nicely formatted task-objectives right in terminal with
group separation, nice progress/status symbols, terminal-fitting design,
minimal statistics per group, overall statistics, start date, finish date,
archiving multi-group tasks and navigating through archive with keys UI.

constraints:
- minimal terminal columns/lines == 80x20
- minimal group name characters == 50
- minimal tasks per group == 50
- adding task convention:
to avoid archive show error you should when
adding description to task use spaces for example
this is my new task or underlines and anything else
if your task will not exceede terminal width,
this_is_ok_task_add since it's not wider than terminal.
"""

from arc.interface import Interface


if __name__ == '__main__':
    Interface().initialize_args()
