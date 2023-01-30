import os
import sys
import json
from arc.resolve import DIR_PATH as dir_path
from arc.log import DebugLog
from arc.archive import Archive, ArchiveUI


class JsonInteraction:
    """Class as a driver between program operations and json file i/o."""
    json_path = os.path.join(dir_path, 'arc.json')
    archive_path = os.path.join(dir_path, 'archive.json')
    json_object = {'all': []}  # main json object for storing groups array

    def _json_decode_resolve(self, path) -> bool:
        """Internal function for resolving json problems."""
        try:
            opened_file = open(path, 'r')
            json_dict = json.load(opened_file)
            if isinstance(json_dict['all'], list):
                opened_file.close()
                return True
            else:
                raise KeyError("main object is not 'all'")

        except KeyError:
            DebugLog().log_exception()
            self.json_dump(self.json_object)
            return True

        except PermissionError:
            DebugLog().log_exception()
            print('error: permission denied')
            sys.exit(1)

        except FileNotFoundError:
            json_object = json.dumps(self.json_object, indent=4)
            with open(path, 'w') as newfile:
                newfile.write(json_object)
                newfile.close()
            return True

        except json.decoder.JSONDecodeError:
            DebugLog().log_exception()
            self.json_dump(self.json_object, json_file=path)
            return True

    def json_load(self, json_file=json_path):
        # decode json to dict
        is_true = self._json_decode_resolve(json_file)
        if is_true:
            opened_file = open(json_file, 'r')
            json_dict = json.load(opened_file)
            opened_file.close()
            return json_dict

    def json_dump(self, json_dict, json_file=json_path):
        # encode dict to json
        is_true = self._json_decode_resolve(json_file)
        if is_true:
            opened_file = open(json_file, 'w')
            json.dump(json_dict, opened_file, indent=4)
            opened_file.close()

    def json_reset(self):
        # method to remove all user entries in arc.json file
        try:
            confirm = input('Are u sure? y/n: ')
            if confirm.lower() == 'y':
                self.json_dump(self.json_object)
                print('all entries are nullified.')
                print('logs are unchanged.')
            else:
                print('reset aborted...')
                sys.exit(0)

        except KeyboardInterrupt:
            DebugLog().log_exception()
            sys.exit(1)

    def user_entries(self):
        # method to check if there is user entries
        json_entries = self.json_load()
        check_group_entries = json_entries['all']

        if check_group_entries != []:
            return True
        else:
            return False

    def index_assign(self, json_list):
        """Method for assigning id_keys to groups/tasks,
        first condition is only applicable to first group+task created."""
        if not self.user_entries():
            return 1
        else:
            highest_id_key = json_list[-1]['id_key']
            new_highest_id_key = highest_id_key + 1
            return new_highest_id_key

    def enum_index(self, json_list):
        """Method for enumerating json indexes."""
        id_key = 1
        for item in json_list:
            item.update({'id_key': id_key})
            id_key += 1
        return json_list

    def change_group_name(self, *args):
        """Method for changing group name."""
        json_entries = self.json_load()
        group_id_key = args[0]
        new_group_name = args[1]

        group = json_entries['all'][group_id_key]
        group['name'] = new_group_name
        self.json_dump(json_entries)

    def expand_task_description(self, *args):
        """Method for getting full task description,
        in case: formatted task can't full fit in terminal size."""
        json_entries = self.json_load()
        group_id_key = args[0]
        task_id_key = args[1]

        task = json_entries['all'][group_id_key]['tasks'][task_id_key]
        print(task['desc'])

    def archive_group(self, group_id_key, archive_name):
        """Method for archiving whole group,
        deleting group and calling enum_index and returning object for log."""
        json_entries = self.json_load()
        archive_entries = self.json_load(json_file=self.archive_path)

        for_log = json_entries['all'][group_id_key]
        out = Archive().transform(for_log, archive_name)

        archive_entries['all'].append(out)
        self.json_dump(archive_entries, json_file=self.archive_path)

        del json_entries['all'][group_id_key]
        self.enum_index(json_entries['all'])
        self.json_dump(json_entries)
        return for_log

    def purge_group(self, group_id_key):
        """Method for purging whole group and task entries, enumerating
        group indexes and returning object for log."""
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

        for_log = json_entries['all'][group_id_key]

        del json_entries['all'][group_id_key]
        self.enum_index(json_entries['all'])
        self.json_dump(json_entries)
        return for_log

    def show_archive(self):
        """Show archive with curses library."""
        archive = self.json_load(json_file=JsonInteraction.archive_path)
        format_arhive = Archive().stack(archive)
        ArchiveUI(format_arhive).run()
