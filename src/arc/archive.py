from resolve import now


class Archive:

    def __init__(self):
        """Very simple presentation of archived tasks,
        only two constructors - symbols."""
        self.done = '✔'
        self.not_done = '☐'

    def transform(self, group) -> dict:
        """Method for preparing group and tasks for json store."""
        # get group variables
        name = group['name']
        group_dict = {'date': now, 'name': name, 'tasks': []}

        # get task variables
        for task in group['tasks']:
            if task['status'] == 'done':
                task_status = True
            else:
                task_status = False
            task_name = task['desc']
            task_dict = {'completion': task_status, 'name': task_name}

            # insert task object in group object
            group_dict['tasks'].append(task_dict)

        # return: json object ready
        return group_dict

    def stack(self, archive) -> str:
        """Method for creating string from archive json store."""
        task_archive = """"""
        groups = archive['all']

        # get group variables
        for group in groups:
            archive_date = group['date']
            group_name = group['name']
            # compose string from group variables
            task_archive = task_archive + f'\n [{archive_date}] [{group_name}]'

            # get task variables
            for task in group['tasks']:
                if task['completion'] is True:
                    task_symb = self.done
                    task_name = task['name']
                else:
                    task_symb = self.not_done
                    task_name = task['name']
                # compose string from task variables
                task_archive = task_archive + f'\n {task_symb} {task_name}'
            # add a column between groups
            task_archive = task_archive + '\n'

        # return: complete groups/tasks string, ready for presentation
        return task_archive


class ArchiveCurses:
    pass
