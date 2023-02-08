"""
< name: arc-tasks >
< author: Predrag Bunic >
< contact: pbunic@proton.me >
< source: github.com/noctdruid/arc-tasks >
< license: GPL v3 >

'arc-tasks' is minimalistic program designed for command-line-interface,
working with asci escape sequences supported terminals, handy with drop-down
terminals, nicely formatted task-objectives right in terminal with
group separation, nice progress/status symbols, terminal-fitting design,
minimal statistics per group, overall statistics, start date, finish date,
archiving multi-group tasks and navigating through archive with UI."""

from arc.interface import Interface


if __name__ == '__main__':
    Interface().initialize_args()
