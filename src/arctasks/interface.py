"""Command-line interface and cli-restrictions."""

import argparse
import os
import sys
from arctasks.log import DebugLog
from arctasks.operations import Operations
from arctasks.resolve import InitCheckout


class Interface:
    """Building argparse library interface."""

    def __init__(self):
        """Add cli arguments.
        :func parser: argparse configurator,
        :func parser.add_argument: configuring cli argument option
        and expected specification of inputs."""

        self.parser = argparse.ArgumentParser(
            prog='arc-tasks',
            description='Minimalistic cli task-objectives tracking.',
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
            type=str, nargs=2
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
            '--append', action='store', dest='append',
            type=str, nargs=2
        )
        self.parser.add_argument(
            '--expand', action='store', dest='expand',
            type=int, nargs=2
        )
        self.parser.add_argument(
            '--show', action='store_true', dest='show',
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

    def _cli_policy(self):
        """Method to adjust user-behaviour inputs."""
        if sys.argv[0] == sys.argv[-1]:
            # bool - representation of is there user-input args?
            return False

        max_args = 1
        mixed_type = ['task', 'group', 'edit', 'archive', 'append']
        args = vars(self.parser.parse_args())

        # loop to check if there is more than one opt
        try:
            input_args = 0
            for key, value in args.items():
                if value:
                    input_args += 1
                    if input_args > max_args:
                        raise SyntaxError('more than one arg forbidden')

        except SyntaxError:
            DebugLog().log_exception()
            sys.exit('error: only one option allowed per execution.')

        # isolate right key-value
        for key, value in args.items():
            if value:
                pair = (key, value)
                break

        # for multi-type cases convert numbers from str to int type
        if pair[0] in mixed_type:
            try:
                if (pair[0] == mixed_type[0] or pair[0] == mixed_type[1] or
                        pair[0] == mixed_type[3] or pair[0] == mixed_type[4]):
                    pair[1][0] = int(pair[1][0])
                elif pair[0] == mixed_type[2]:
                    pair[1][0] = int(pair[1][0])
                    pair[1][1] = int(pair[1][1])

            except ValueError:
                DebugLog().log_exception()
                sys.exit('error: wrong argument value provided.')

        return pair

    def initialize_args(self):
        """Method to initialize argparse cli."""
        # check if there is problem with directory
        try:
            if InitCheckout().dir_check():
                # directory is regular
                pass
            else:
                # problem with directory existence/permission or
                # different type of problem unknown
                raise OSError

        except OSError:
            # exit program and deliver notification
            user = os.getenv('USER')
            DebugLog().log_exception()
            sys.exit(f'directory error: /home/{user}/.arc-tasks/')

        # Isolated cli entry
        args = self._cli_policy()

        # Dict for program operations
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
            'archive': 'Operations().single().archive(args[1][0], args[1][1])',
            'purge': 'Operations().single().purge(*args[1])',
            'start': 'Operations().multi().start(*args[1])',
            'finish': 'Operations().multi().finish(*args[1])',
            'board': 'Operations().special().board()',
            'append':
                'Operations().special().append_archive(args[1][0],args[1][1])',
            'expand': 'Operations().special().expand(args[1][0], args[1][1])',
            'show': 'Operations().special().show()',
            'reset': 'Operations().special().reset()',
            'help': 'Operations().special().help_()',
            'usage': 'Operations().special().usage()',
        }

        # condition: if there is or there is not user cli inputs
        if args is False:
            # No inputs, default command is --board
            Operations().special().board()
        else:
            # There is input(s), eval dict str
            eval(action_library[args[0]])
