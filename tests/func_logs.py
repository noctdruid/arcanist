import os
import sys
sys.path.append(os.path.abspath('../src/arc/'))

from log import DebugLog, InfoLog


class LogTest:
    def test_debug(self):
        try:
            x = -1
            if x < 0:
                raise TypeError('error: int needs to be positive')
        except TypeError:
            DebugLog().log_exception()

    def test_info(self):
        InfoLog().log_entry((
            'create',
            'MyGroup',
            'MyTask',
        ))

        InfoLog().log_entries((
            ('archive', 'zen of python'),
            ('task1', 'task2', 'task3')
        ))

        InfoLog().log_rename((
            ('rename group', 'Old Group Name __-->__ New Group Name')
        ))


if __name__ == '__main__':
    try:
        if sys.argv[1] == '--debug':
            LogTest().test_debug()
            print('done, check debug.log')

        elif sys.argv[1] == '--info':
            LogTest().test_info()
            print('done, check store.log')
        else:
            print('usage: python3 log_entry.py <arg>')
            print('args: --debug or --info')
    except IndexError:
        print('error: provide cli argument')
        print('args: --debug or --info')
