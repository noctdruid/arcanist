import argparse
import sys
from log import DebugLog
from operations import Operations


class Interface:
    """ doc """
    def _init_args(self):
        self.parser = argparse.ArgumentParser(
            prog='arc-tasks',
            description='Minimalistic command-line task objectives tracking.',
            usage='%(prog)s [OPTS]',
            add_help=False
        )

        self.parser.add_argument(
            '-c', '--create', action='store', dest='create',
            type=str, nargs=2
        )
        self.parser.add_argument(
            '-t', '--task', action='store', dest='task',
            type=str, nargs=2
        )
        self.parser.add_argument(
            '-g', '--group', action='store', dest='group',
            type=str, nargs=2
        )
        self.parser.add_argument(
            '-e', '--edit', action='store', dest='edit',
            type=str, nargs=3
        )
        self.parser.add_argument(
            '-r', '--remove', action='store', dest='remove',
            type=int, nargs=2
        )
        self.parser.add_argument(
            '-a', '--archive', action='store', dest='archive',
            type=int, nargs=1
        )
        self.parser.add_argument(
            '-p', '--purge', action='store', dest='purge',
            type=int, nargs=1
        )
        self.parser.add_argument(
            '-s', '--start', action='store', dest='start',
            type=int, nargs='*'
        )
        self.parser.add_argument(
            '-f', '--finish', action='store', dest='finish',
            type=int, nargs='*'
        )
        self.parser.add_argument(
            '--board', action='store_true', dest='board'
        )
        self.parser.add_argument(
            '--expand', action='store', dest='expand',
            type=int, nargs=2
        )
        self.parser.add_argument(
            '--reset', action='store_true', dest='reset'
        )
        self.parser.add_argument(
            '--help', action='store_true', dest='help'
        )
        self.parser.add_argument(
            '--usage', action='store_true', dest='usage'
        )

        args = self.parser.parse_args()
        return args

    def _cli_policy(self):
        """ doc """
        if sys.argv[0] == sys.argv[-1]:
            return False

        MAX_ARGS = 1
        MIXED_TYPE = ['task', 'group', 'edit']
        args = vars(self._init_args())

        # loop to check if there is more than one opt
        try:
            input_args = 0
            for key, value in args.items():
                if value:
                    input_args += 1
                    if input_args > MAX_ARGS:
                        raise SyntaxError('multiple options input.')

        except SyntaxError:
            print('error: only one option allowed.')
            DebugLog().log_exception()
            sys.exit(1)

        # isolate right key-value, get rid of others
        for key, value in args.items():
            if value:
                pair = (key, value)
            break

        # for multi-type cases convert numbers to int type
        if pair[0] in MIXED_TYPE:
            try:
                if pair[0] == MIXED_TYPE[0] or pair[0] == MIXED_TYPE[1]:
                    pair[1][0] = int(pair[1][0])
                elif pair[0] == MIXED_TYPE[2]:
                    pair[1][0] = int(pair[1][0])
                    pair[1][1] = int(pair[1][1])

            except ValueError:
                print('error: wrong argument value provided.')
                DebugLog().log_exception()
                sys.exit(1)

        return pair

    def initialize_args(self):
        """ ... """
        args = self._cli_policy()
        action_library = {
            'create':
                'Operations().single(group_name=args[1][0],' +
                'task_name=args[1][1]).create()',

            'task':
                'Operations().single(group_id_key=args[1][0],' +
                'task_name=args[1][1]).task()',

            'group':
                'Operations().single(group_id_key=args[1][0],' +
                'group_name=args[1][1]).group()',

            'edit':
                'Operations().single(group_id_key=args[1][0],' +
                'task_id_key=args[1][1],task_name=args[1][2]).edit()',

            'remove':
                'Operations().single(group_id_key=args[1][0],' +
                'task_id_key=args[1][1]).remove()',

            'archive': 'Operations().single().archive(*args[1])',
            'purge': 'Operations().single().purge(*args[1])',
            'start': 'Operations().multi().start(*args[1])',
            'finish': 'Operations().multi().finish(*args[1])',
            'board': 'Operations().special().board()',
            'expand': 'Operations().special().expand(args[1][0], args[1][1])',
            'reset': 'Operations().special().reset()',
            'help': 'Operations().special().help_()',
            'usage': 'Operations().special().usage()',
        }

        if args is False:
            Operations().special().board()
        else:
            eval(action_library[args[0]])
