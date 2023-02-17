import os
import sys
import unittest
sys.path.append(os.path.abspath('../src/'))

from arctasks.jsonpy import JsonInteraction
from arctasks.operations import Operations

output_null = open('/dev/null', 'w')
sys.stdout = output_null


class OperationsTestCase(unittest.TestCase):
    def test_create(self):
        JsonInteraction().json_dump({'all': []})

        Operations().single(group_name='1st', task_name='1st').create()
        Operations().single(group_name='2nd', task_name='1st').create()
        Operations().single(group_name='3rd', task_name='1st').create()

        json_obj = JsonInteraction().json_load()
        total = 0
        for i in json_obj['all']:
            total += 1
            for j in i['tasks']:
                total += 1

        self.assertEqual(total, 6)
        JsonInteraction().json_dump({'all': []})

    def test_task(self):
        JsonInteraction().json_dump({'all': []})

        Operations().single(group_name='1st', task_name='1st').create()
        Operations().single(group_name='2nd', task_name='1st').create()
        Operations().single(group_name='3rd', task_name='1st').create()
        Operations().single(group_id_key=2, task_name='2nd').task()
        Operations().single(group_id_key=2, task_name='3rd').task()

        json_obj = JsonInteraction().json_load()
        total = 0
        for i in json_obj['all']:
            total += 1
            for j in i['tasks']:
                total += 1

        self.assertEqual(total, 8)
        JsonInteraction().json_dump({'all': []})

    def test_group_task_edit(self):
        JsonInteraction().json_dump({'all': []})

        Operations().single(group_name='1st', task_name='1st').create()
        Operations().single(group_id_key=1, group_name='N E W').group()
        Operations().single(
            group_id_key=1, task_id_key=1, task_name='changed task.'
        ).edit()

        json_obj = JsonInteraction().json_load()
        extract_group_name = json_obj['all'][0]['name']
        self.assertEqual(extract_group_name, 'N E W')
        extract_task_name = json_obj['all'][0]['tasks'][0]['desc']
        self.assertEqual(extract_task_name, 'changed task.')
        JsonInteraction().json_dump({'all': []})

    def test_start_end_task(self):
        JsonInteraction().json_dump({'all': []})

        Operations().single(group_name='TEST', task_name='first').create()
        Operations().single(group_id_key=1, task_name='second').task()
        Operations().single(group_id_key=1, task_name='third').task()
        Operations().single(group_id_key=1, task_name='four').task()
        Operations().single(group_id_key=1, task_name='five').task()

        Operations().multi().start(1, 1, 2, 3)
        Operations().multi().finish(1, 4, 5)
        json_obj = JsonInteraction().json_load()

        total_inprog = 0
        total_done = 0

        for i in json_obj['all'][0]['tasks']:
            if i['status'] == 'inprog':
                total_inprog += 1
            elif i['status'] == 'done':
                total_done += 1
            else:
                pass

        self.assertEqual(total_inprog, 3)
        self.assertEqual(total_done, 2)
        JsonInteraction().json_dump({'all': []})

    def test_reverse(self):
        JsonInteraction().json_dump({'all': []})

        Operations().single(group_name='TEST', task_name='first').create()
        Operations().single(group_id_key=1, task_name='second').task()
        Operations().single(group_id_key=1, task_name='third').task()
        Operations().single(group_id_key=1, task_name='four').task()
        Operations().single(group_id_key=1, task_name='five').task()

        Operations().multi().start(1, 1, 2, 3)
        Operations().multi().finish(1, 4, 5)

        Operations().multi().start(1, 1, 3, 5)
        Operations().multi().finish(1, 2, 4)

        json_obj = JsonInteraction().json_load()
        pending = 0  # 3
        inprog = 0  # 1
        done = 0  # 1

        for i in json_obj['all'][0]['tasks']:
            print(i['status'])
            if i['status'] == 'pending':
                pending += 1
            elif i['status'] == 'inprog':
                inprog += 1
            elif i['status'] == 'done':
                done += 1
            else:
                raise IndexError('???')

        total = [pending, inprog, done]
        self.assertEqual(total, [3, 1, 1])
        JsonInteraction().json_dump({'all': []})


if __name__ == '__main__':
    unittest.main()
    output_null.close()
