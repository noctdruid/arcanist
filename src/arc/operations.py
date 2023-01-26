from arc.resolve import now
from arc.jsonpy import JsonInteraction
from arc.log import InfoLog
from arc.board import Board
from arc.doc import Man, Notifications


class Group:
    """Group composition."""
    def __init__(self, id_key, name):
        self.id_key = id_key
        self.name = name
        self.tasks = []

    def make_group(self):
        f_dict = self.__dict__
        return f_dict


class Task:

    def __init__(self, **kwargs):
        """Clas for task value changes.
        :param kwargs: different task construction attributes,
        :attr end: hypothetical end-date placeholder. """
        self.kwargs = kwargs
        self.end_ = '     -     '

    def new_task(self):
        """Base task construction."""
        id_key = self.kwargs['id_key']
        task_desc = self.kwargs['task_desc']
        task = {
            'id_key': id_key,
            'status': 'pending',
            'start': now,
            'end': self.end_,
            'desc': task_desc
        }
        return task

    # task-changes
    def start_task(self):
        task = {'status': 'inprog', 'end': self.end_}
        return task

    def finish_task(self):
        task = {'status': 'done', 'end': now}
        return task

    def reverse_task(self):
        task = {'status': 'pending', 'end': self.end_}
        return task


class Operations:

    def __init__(self):
        """doc"""
        self.single = self.SingleOperations
        self.multi = self.MultiOperations
        self.special = self.SpecialOperations

    class SingleOperations:
        """ Class for single-input/positional operations """
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.json_obj = JsonInteraction().json_load()

        def create(self):
            group_name = self.kwargs['group_name']
            task_name = self.kwargs['task_name']
            json_obj = self.json_obj['all']

            get_id = JsonInteraction().index_assign(json_obj)
            group_inst = Group(get_id, group_name).make_group()
            task_inst = Task(id_key=1, task_desc=task_name).new_task()
            group_inst['tasks'].append(task_inst)
            json_obj.append(group_inst)
            JsonInteraction().json_dump(self.json_obj)

            # InfoLog
            InfoLog().log_entry(
                ('create group and task', group_name, task_name)
            )

            # Notification
            print(Notifications().notify('create', group_name, task_name))

        def task(self):
            group_id_key = self.kwargs['group_id_key'] - 1
            task_name = self.kwargs['task_name']
            json_obj = self.json_obj['all'][group_id_key]['tasks']
            get_id = JsonInteraction().index_assign(json_obj)
            task_inst = Task(id_key=get_id, task_desc=task_name).new_task()
            json_obj.append(task_inst)
            JsonInteraction().json_dump(self.json_obj)

            # InfoLog
            group_name = self.json_obj['all'][group_id_key]['name']
            InfoLog().log_entry(
                ('add task', group_name, task_name)
            )

            # Notification
            print(Notifications().notify('task', task_name, group_name))

        def group(self):
            group_id_key = self.kwargs['group_id_key'] - 1
            group_name = self.kwargs['group_name']
            old_name = self.json_obj['all'][group_id_key]['name']
            JsonInteraction().change_group_name(group_id_key, group_name)

            # InfoLog
            InfoLog().log_rename(
                ('rename group', f'{old_name} __-->__ {group_name}')
            )

            # Notification
            print(Notifications().notify('group', old_name, group_name))

        def edit(self):
            group_id_key = self.kwargs['group_id_key'] - 1
            task_id_key = self.kwargs['task_id_key'] - 1
            task_name = self.kwargs['task_name']
            json_obj = self.json_obj['all'][group_id_key]['tasks'][task_id_key]
            old_name = json_obj['desc']
            json_obj['desc'] = task_name
            JsonInteraction().json_dump(self.json_obj)

            # InfoLog
            group_name = self.json_obj['all'][group_id_key]['name']
            InfoLog().log_entry(
                ('edit task description',
                 group_name, f'{old_name} __-->__ {task_name}')
            )

            # Notification
            print(Notifications().notify(
                'edit', group_name, old_name, task_name
                )
            )

        def remove(self):
            group_id_key = self.kwargs['group_id_key'] - 1
            task_id_key = self.kwargs['task_id_key'] - 1
            json_obj = self.json_obj['all'][group_id_key]['tasks']
            task_name = json_obj[task_id_key]['desc']
            del json_obj[task_id_key]

            if json_obj:
                JsonInteraction().enum_index(json_obj)
            elif not json_obj:
                del self.json_obj['all'][group_id_key]

            JsonInteraction().json_dump(self.json_obj)

            # InfoLog
            group_name = self.json_obj['all'][group_id_key]['name']
            InfoLog().log_entry(
                ('remove task', group_name, task_name)
            )

            # Notification
            print(Notifications().notify('remove', task_name, group_name))

        def archive(self, group_id_key):
            group = JsonInteraction().archive_group(group_id_key - 1)
            cmd = 'archive group'
            group_name = group['name']
            tasks = group['tasks']

            list_of_tasks = []
            for task in tasks:
                list_of_tasks.append(task['desc'])

            InfoLog().log_entries((
                (cmd, group_name),
                list_of_tasks
            ))

            # Notification
            print(Notifications().notify('archive', group_name))

        def purge(self, group_id_key):
            group = JsonInteraction().purge_group(group_id_key - 1)
            cmd = 'purge group'
            group_name = group['name']
            tasks = group['tasks']

            list_of_tasks = []
            for task in tasks:
                list_of_tasks.append(task['desc'])

            InfoLog().log_entries((
                (cmd, group_name),
                list_of_tasks
            ))

            # Notification
            print(Notifications().notify('purge', group_name))

    class MultiOperations:
        """ This class is for start/finish options,
        it supports multi-inputs """
        def __init__(self):
            self.json_obj = JsonInteraction().json_load()

        def start(self, *args):
            group = self.json_obj['all'][args[0] - 1]['tasks']
            list_of_keys = [x + 1 for x in range(len(group))]

            for arg in args[1:]:
                if arg not in list_of_keys:
                    print(f"wrong task_id_key: {arg}")

                elif group[arg - 1]['status'] == 'inprog':
                    print(
                        f"{group[arg - 1]['desc']}: " +
                        "'IN-PROGRESS __-->__ PENDING'"
                    )
                    new_attr = Task().reverse_task()
                    for key, value in group[arg - 1].items():
                        try:
                            if group[arg - 1][key] != new_attr[key]:
                                group[arg - 1][key] = new_attr[key]
                        except KeyError:
                            pass

                else:
                    if group[arg - 1]['status'] == 'pending':
                        old_status = 'PENDING'
                    else:
                        old_status = 'DONE'
                    print(
                        f"{group[arg - 1]['desc']}: " +
                        f"'{old_status} __-->__ IN-PROGRESS'"
                    )
                    new_attr = Task().start_task()
                    for key, value in group[arg - 1].items():
                        try:
                            if group[arg - 1][key] != new_attr[key]:
                                group[arg - 1][key] = new_attr[key]
                        except KeyError:
                            pass

            JsonInteraction().json_dump(self.json_obj)

        def finish(self, *args):
            group = self.json_obj['all'][args[0] - 1]['tasks']
            list_of_keys = [x + 1 for x in range(len(group))]

            for arg in args[1:]:
                if arg not in list_of_keys:
                    print(f'wrong task_id_key: {arg}')

                elif group[arg - 1]['status'] == 'done':
                    print(
                        f"{group[arg - 1]['desc']}: " +
                        "'DONE __-->__ PENDING'"
                    )
                    new_attr = Task().reverse_task()
                    for key, value in group[arg - 1].items():
                        try:
                            if group[arg - 1][key] != new_attr[key]:
                                group[arg - 1][key] = new_attr[key]
                        except KeyError:
                            pass

                else:
                    if group[arg - 1]['status'] == 'pending':
                        old_status = 'PENDING'
                    else:
                        old_status = 'IN-PROGRESS'
                    print(
                        f"{group[arg - 1]['desc']}: " +
                        f"'{old_status} __-->__ DONE'"
                    )
                    new_attr = Task().finish_task()
                    for key, value in group[arg - 1].items():
                        try:
                            if group[arg - 1][key] != new_attr[key]:
                                group[arg - 1][key] = new_attr[key]
                        except KeyError:
                            pass

            JsonInteraction().json_dump(self.json_obj)

    class SpecialOperations:
        """ Class intended only for output operations """
        def __init__(self):
            self.json_obj = JsonInteraction().json_load()

        def board(self):
            if JsonInteraction().user_entries():
                json_obj = self.json_obj['all']

                for group in json_obj:
                    done_t = 0
                    total_t = group['tasks'][-1]['id_key']
                    for check_task in group['tasks']:
                        if check_task['status'] == 'done':
                            done_t += 1

                    print(Board().group_formatting(
                        group['id_key'], group['name'], done_t, total_t)
                    )

                    print(Board().column_formatting())
                    for task in group['tasks']:
                        f_task = Board().task_formatting(
                            task['id_key'],
                            task['status'],
                            task['start'],
                            task['end'],
                            task['desc']
                        )
                        print(f_task)

                done = 0
                doing = 0
                not_done = 0

                for group in json_obj:
                    for task in group['tasks']:
                        if task['status'] == 'done':
                            done += 1
                        elif task['status'] == 'inprog':
                            doing += 1
                        else:
                            not_done += 1

                statistics_f = \
                    Board()._statistics(done, doing, not_done)
                print(f'\n    {statistics_f[0]}')
                print(f'    {statistics_f[1]}\n')

            else:
                print('no task entries, try --help or --guide.')

        def expand(self, *id_keys):
            JsonInteraction().expand_task_description(
                id_keys[0] - 1, id_keys[1] - 1
            )

        def show(self):
            JsonInteraction().show_archive()

        def reset(self):
            JsonInteraction().json_reset()

        def help_(self):
            print(Man.HELP)

        def usage(self):
            print(Man.USAGE)
