import os
import sys
import json
from resolve import DIR_PATH
from log import DebugLog


class JsonInteraction:
    """ Class as a driver between program operations and json i/o """
    json_path = os.path.join(DIR_PATH, 'store.json')
    json_object = {'all': []}  # main json object for storing groups array

    def json_load(self, json_file=json_path):
        # json decode to dict
        try:
            opened_file = open(json_file, 'r')
            json_dict = json.load(opened_file)
            opened_file.close()
            return json_dict

        except FileNotFoundError:
            print("error: file not found, check ~/.arc-tasks/debug.log")
            DebugLog().log_exception()
            sys.exit(1)

        except PermissionError:
            print(
                "error: file doesn't have right permissions, " +
                "check ~/.arc-tasks/debug.log"
            )
            DebugLog().log_exception()
            sys.exit(1)

        except json.decoder.JSONDecodeError:
            print("error: json decoder, trying to resolve... exec cmd again")
            DebugLog().log_exception()
            self.json_dump(self.json_object)
            sys.exit(1)

    def json_dump(self, json_dict, json_file=json_path):
        # encode dict to json
        try:
            opened_file = open(json_file, 'w')
            json.dump(json_dict, opened_file, indent=4)
            opened_file.close()

        except PermissionError:
            print(
                "error: file doesn't have right permissions, " +
                "check ~/.arc-tasks/debug.log"
            )
            DebugLog().log_exception()
            sys.exit(1)

    def json_reset(self, json_file=json_path):
        # method to remove all user entries in json file
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
        # method for assigning id_keys to groups/tasks
        # first condition is only applicable to first group+task created
        if not self.user_entries():
            return 1
        else:
            highest_id_key = json_list[-1]['id_key']
            new_highest_id_key = highest_id_key + 1
            return new_highest_id_key

    def enum_index(self, json_list):
        # method for enumerating json indexes
        id_key = 1
        for item in json_list:
            item.update({'id_key': id_key})
            id_key += 1
        return json_list

    def change_group_name(self, *args):
        # method for changing group name
        json_entries = self.json_load()
        group_id_key = args[0]
        new_group_name = args[1]

        group = json_entries['all'][group_id_key]
        group['name'] = new_group_name
        self.json_dump(json_entries)

    def expand_task_description(self, *args):
        # method for getting full task description,
        # in case: formatted task can't full fit in terminal size
        json_entries = self.json_load()
        group_id_key = args[0]
        task_id_key = args[1]

        task = json_entries['all'][group_id_key]['tasks'][task_id_key]
        print(task['desc'])

    def purge_group(self, group_id_key):
        # method for deleting whole group,
        # enumerating indexes and returning object for log
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

        if json_entries['all']:
            self.enum_index(json_entries['all'])

        self.json_dump(json_entries)
        return for_log
