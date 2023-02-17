"""Interaction with json files."""

import os
import sys
import json
from arctasks.resolve import DIR_PATH as dir_path
from arctasks.log import DebugLog
from arctasks.archive import Archive, ArchiveUI


class JsonInteraction:
    """Class as a driver between program operations and json file i/o."""
    json_path = os.path.join(dir_path, 'arc.json')
    archive_path = os.path.join(dir_path, 'archive.json')
    json_object = {'all': []}  # main json object for storing groups array

    def _json_decode_resolve(self, path) -> bool:
        """Internal function for resolving json problems."""
        try:
            opened_file = open(path, 'r', encoding='utf-8')
            json_dict = json.load(opened_file)
            if isinstance(json_dict['all'], list):
                opened_file.close()
            else:
                raise KeyError("main object is not 'all'")

        except KeyError:
            DebugLog().log_exception()
            self.json_dump(self.json_object)

        except PermissionError:
            DebugLog().log_exception()
            sys.exit('error: permission denied')

        except FileNotFoundError:
            DebugLog().log_exception()
            json_object = json.dumps(self.json_object, indent=4)
            with open(path, 'w', encoding='utf-8') as newfile:
                newfile.write(json_object)
                newfile.close()

        except json.decoder.JSONDecodeError:
            DebugLog().log_exception()
            self.json_dump(self.json_object, json_file=path)

        # No error triggered or errors resolved
        return True

    def json_load(self, json_file=json_path):
        """Decode json to dict."""
        is_true = self._json_decode_resolve(json_file)
        if is_true:
            opened_file = open(json_file, 'r', encoding='utf-8')
            json_dict = json.load(opened_file)
            opened_file.close()
            return json_dict
        return None

    def json_dump(self, json_dict, json_file=json_path):
        """Encode dict to json."""
        is_true = self._json_decode_resolve(json_file)
        if is_true:
            opened_file = open(json_file, 'w', encoding='utf-8')
            json.dump(json_dict, opened_file, indent=4)
            opened_file.close()

    def json_reset(self):
        """Remove all user entries in arc.json file."""
        try:
            confirm = input('Are u sure? y/n: ')
            if confirm.lower() == 'y':
                self.json_dump(self.json_object)
                print('all entries are nullified.')
                print('archive and logs unchanged.')
            else:
                sys.exit('reset aborted...')

        except KeyboardInterrupt:
            DebugLog().log_exception()
            sys.exit(1)

    def user_entries(self):
        """Check if there is user entries."""
        json_entries = self.json_load()
        check_group_entries = json_entries['all']

        if check_group_entries != []:
            return True
        return False

    def index_assign(self, json_list):
        """Assigning id_keys to groups/tasks, first condition
        is only applicable to the first group+task created."""
        if not self.user_entries():
            return 1
        highest_id_key = json_list[-1]['id_key']
        new_highest_id_key = highest_id_key + 1
        return new_highest_id_key

    def enum_index(self, json_list):
        """Enumerating json indexes."""
        id_key = 1
        for item in json_list:
            item.update({'id_key': id_key})
            id_key += 1
        return json_list

    def change_group_name(self, *args):
        """Changing group name."""
        json_entries = self.json_load()
        group_id_key = args[0]
        new_group_name = args[1]

        group = json_entries['all'][group_id_key]
        group['name'] = new_group_name
        self.json_dump(json_entries)

    def expand_task_description(self, *args):
        """Getting full task description, in case:
        formatted task can't fully fit in terminal size."""
        json_entries = self.json_load()
        group_id_key = args[0]
        task_id_key = args[1]

        task = json_entries['all'][group_id_key]['tasks'][task_id_key]
        print(task['desc'])

    def archive_group(self, group_id_key, archive_name):
        """Creating archive, archiving tasks and cleaning."""
        json_entries = self.json_load()
        archive_entries = self.json_load(json_file=self.archive_path)

        # User-entry validation
        archive_names = []
        for archive in archive_entries['all']:
            archive_names.append(archive['name'])

        if archive_name not in archive_names:
            pass
        else:
            sys.exit(f"err: '{archive_name}' __<--__ already exists")

        # Archiving group
        group_info = json_entries['all'][group_id_key]
        tasks_out = Archive().transform(group_info, archive_name)
        archive_entries['all'].append(tasks_out)
        self.json_dump(archive_entries, json_file=self.archive_path)

        # Cleaning
        del json_entries['all'][group_id_key]
        self.enum_index(json_entries['all'])
        self.json_dump(json_entries)

        return group_info

    def append_archive(self, group_id_key, archive_name):
        """Appending tasks to archive and cleaning."""
        json_entries = self.json_load()
        archive_entries = self.json_load(json_file=self.archive_path)

        # User-entry validation and array archive matching
        archive_names = []
        archive_id = 0
        for archive in archive_entries['all']:
            if archive['name'] == archive_name:
                archive_names.append(archive['name'])
                break
            archive_names.append(archive['name'])
            archive_id += 1

        if archive_name in archive_names:
            pass
        else:
            sys.exit(f"'{archive_name}' __<--__ archive doesn't exist")

        # Archiving additional tasks
        group_info = json_entries['all'][group_id_key]
        tasks_out = Archive().transform(group_info)
        tasks = archive_entries['all'][archive_id]['tasks']
        for task in tasks_out['tasks']:
            # Adding task by task in archive
            tasks.append(task)
        self.json_dump(archive_entries, json_file=self.archive_path)

        # Cleaning
        del json_entries['all'][group_id_key]
        self.enum_index(json_entries['all'])
        self.json_dump(json_entries)

        return group_info

    def purge_group(self, group_id_key):
        """Purging whole group/task entries and cleaning."""
        json_entries = self.json_load()
        try:
            confirm = input('Are u sure? y/n: ')
            if confirm.lower() == 'y':
                pass
            else:
                print('purge aborted...')
                sys.exit(0)

        except KeyboardInterrupt:
            DebugLog().log_exception()
            sys.exit(1)

        group_info = json_entries['all'][group_id_key]

        # Cleaning
        del json_entries['all'][group_id_key]
        self.enum_index(json_entries['all'])
        self.json_dump(json_entries)

        return group_info

    def show_archive(self):
        """Show archive with curses library."""
        archive = self.json_load(json_file=JsonInteraction.archive_path)
        format_archive = Archive().stack(archive)
        ArchiveUI(format_archive).run()
