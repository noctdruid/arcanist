"""Notifications and manuals output."""


class Man:
    """Multi-line help/guide command outputs."""
    HELP = """
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
    """

    USAGE = """
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
    """


class Notifications:
    """Post command-execution notifications."""
    dictkw = {
        'create': 'new group: %s\nnew task: %s',
        'task': 'task: %s\nassigned to the group: %s',
        'group': 'changed name of the group:\n%s __-->__ %s',
        'edit': 'changed task from the group: %s\n%s __-->__ %s',
        'remove': 'removed task: %s\nfrom the group: %s',
        'archive': 'new archive: %s',
        'purge': 'whole group deleted: %s',
        'append': 'archive: %s __<--__ group append',
    }

    # Notification delivery
    def notify(self, *args) -> str:
        """Notification about operation execution."""
        notification = self.dictkw[args[0]]
        return notification % tuple(args[1:])


# Archive window menu
MENU = '[Q] Quit | [KEY_UP][KEY_DOWN][PGUP][PGDN][HOME][END] \
Navigation | [%d/%d] Page'
