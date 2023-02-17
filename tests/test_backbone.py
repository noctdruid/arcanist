import os
import sys
import unittest
sys.path.append(os.path.abspath('../src/'))

from arctasks.jsonpy import JsonInteraction
from arctasks.resolve import TerminalFormatting


class JsonTestCase(unittest.TestCase):
    def test_json_object(self):
        # test json input/output
        json_obj = {'all': []}
        JsonInteraction().json_dump(json_obj)
        json_output = JsonInteraction().json_load()
        self.assertEqual(json_obj, json_output)

    def test_user_entries(self):
        # test if user_entries() returns False if there is only json object
        json_obj = {'all': []}
        JsonInteraction().json_dump(json_obj)
        user_entries = JsonInteraction().user_entries()
        self.assertFalse(user_entries)

    def test_create_group_task(self):
        # test: making group, making task, assigning id_key
        json_obj = {'all': []}
        JsonInteraction().json_dump(json_obj)
        get_id = JsonInteraction().index_assign(json_obj['all'])
        group_pattern = {
            'id_key': get_id,
            'name': 'MyGroup',
            'tasks': [],
        }
        load = JsonInteraction().json_load()
        load['all'].append(group_pattern)
        pick_element = load['all'][0]
        self.assertEqual(pick_element['id_key'], 1)

        task_pattern = {
            'id_key': 1,
            'status': 'pending',
            'start': '28-DEC-2022',
            'end': '     -     ',
            'desc': 'MyNewTask',
        }
        pick_element['tasks'].append(task_pattern)
        task_attr = pick_element['tasks'][0]['desc']
        self.assertEqual(task_attr, 'MyNewTask')

    def test_other_functions(self):
        # test: enum_index(), change_group_name(), expand_task_description()
        json_obj = {'all': []}
        JsonInteraction().json_dump(json_obj)
        get_id = JsonInteraction().index_assign(json_obj['all'])
        group_pattern = {
            'id_key': get_id,
            'name': 'MyGroup',
            'tasks': [],
        }
        json_obj['all'].append(group_pattern)
        JsonInteraction().json_dump(json_obj)
        JsonInteraction().change_group_name(0, 'NewGroupName')
        is_name_right = JsonInteraction().json_load()
        self.assertEqual(is_name_right['all'][0]['name'], 'NewGroupName')

    def test_group_json_io(self):
        # test group input
        json_obj = {'all': []}
        JsonInteraction().json_dump(json_obj)
        group_pattern = {
            'id_key': 1,
            'name': 'MyGroup',
            'tasks': [],
        }
        json_obj['all'].append(group_pattern)
        JsonInteraction().json_dump(json_obj)
        x = JsonInteraction().json_load()
        self.assertEqual(x['all'][0], group_pattern)


class ResolveTestCase(unittest.TestCase):
    def test_shell_allowed_one(self):
        # test if shell is allowed
        shell_instance = TerminalFormatting()
        shell_instance.user_shell_width = 80
        self.assertTrue(shell_instance.shell_allowed())

    def test_shell_allowed_two(self):
        # test if shell is allowed
        shell_instance = TerminalFormatting()
        shell_instance.user_shell_width = 78
        self.assertFalse(shell_instance.shell_allowed())

    def test_add_space(self):
        # test id_key formatting
        result = TerminalFormatting().add_space(5)
        self.assertEqual(result, ' 5')

    def test_measure_task_desc(self):
        # test string formatting
        my_str = 'this is new task description'
        shell_instance = TerminalFormatting()
        shell_instance.user_shell_width = 80
        result = shell_instance.measure_task_desc(my_str)
        second_result = 35 - len(my_str)
        self.assertEqual(result, second_result)


if __name__ == '__main__':
    unittest.main()
