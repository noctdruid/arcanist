import os
import sys
import unittest
sys.path.append(os.path.abspath('../src/arc/'))

from jsonpy import JsonInteraction
from operations import Operations


class SingleTestCase(unittest.TestCase):
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

    def test_add(self):
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


class MultiTestCase(unittest.TestCase):
    pass


class SpecialTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
