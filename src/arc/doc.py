class Man:
    HELP = """
    usage: arc-tasks [OPT]
    for usage examples type: arc-tasks --usage

    [SINGLE-TASK ARG]
    -c, --create: create group & task
    -t, --task: add task to the group
    -g, --group: change name of the group
    -e, --edit: edit task description
    -r, --remove: remove task
    -a, --archive: archive whole group date-based
    -p, --purge: purge whole group and tasks

    [MULTI-TASK ARGS OR OPERATIONS]
    -s, --start: change state of task(s) to 'in progress'
    -f, --finish: change state of task(s) to 'done'

    [SPECIAL OPERATIONS]
    --board: show tasks board (default)
    --expand: expand task description
    --reset: restart program to no task entries
    --help: show this help message
    --usage: show examples of usage
    """

    USAGE = """
    single-task arg example:
    arc-tasks -c 'name_of_the_group' 'desc_of_a_task'
    arc-tasks -t <group_id> 'desc_of_a_task'
    arc-tasks -g <group_id> 'new_name_of_the_group'
    arc-tasks -e <group_id> <task_id> 'new_desc_of_a_task'
    arc-tasks -r <group_id> <task_id>
    arc-tasks -a <group_id>
    arc-tasks -p <group_id>

    multi-task args example:
    arc-tasks -s <group_id> <task_id> <task_id> ...
    arc-tasks -f <group_id> <task_id> <task_id> ...

    special-operation arg example:
    arc-tasks --expand <group_id> <task_id>
    """


class Notifications:
    kw = {
        'x': 'x',
    }

    def notify(self, *args) -> str:
        pass
