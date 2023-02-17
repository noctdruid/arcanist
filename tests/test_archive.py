import os
import sys
import unittest
sys.path.append(os.path.abspath('../src/'))

from arctasks.archive import Archive


class ArchiveTestCase(unittest.TestCase):

    json_obj = {'all': [{'name': 'MyGroup', 'tasks': [
        {
            'id_key': 1,
            'status': 'pending',
            'start': '28-DEC-2022',
            'end': '     -     ',
            'desc': 'MyNewTask',
        },
        {
            'id_key': 2,
            'status': 'inprog',
            'start': '29-DEC-2022',
            'end': '     -     ',
            'desc': 'Doing this task',
        },
        {
            'id_key': 3,
            'status': 'done',
            'start': '29-DEC-2022',
            'end': '30-DEC-2022',
            'desc': 'Finished task',
        }]
    }]}

    output = Archive().transform(json_obj['all'][0])

    def test_transform_one(self):
        # test group tasks containing and name
        x = self.output['name']
        y = self.output['tasks']
        self.assertEqual(x, None)
        self.assertEqual(len(y), 3)

    def test_transform_two(self):
        # test newly formatted tasks bools
        x = self.output['tasks'][0]
        y = self.output['tasks'][1]
        z = self.output['tasks'][2]
        self.assertEqual(x['completion'], False)
        self.assertEqual(y['completion'], False)
        self.assertEqual(z['completion'], True)

    def test_transform_three(self):
        # test if task names(desc) are same
        x = self.output['tasks'][0]
        y = self.output['tasks'][1]
        z = self.output['tasks'][2]
        self.assertEqual(x['name'], 'MyNewTask')
        self.assertEqual(y['name'], 'Doing this task')
        self.assertEqual(z['name'], 'Finished task')


if __name__ == '__main__':
    unittest.main()
