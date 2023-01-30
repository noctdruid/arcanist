"""Log module informations:
DEBUG FILE LOCATION: /home/$USER/.arc-tasks/debug.log
INFO FILE LOCATION: /home/$USER/.arc-tasks/history.log
FORMAT: 2023-01-05__10:10:19__PM:LEVEL: message
LEVEL DEBUG: exceptions
LEVEL INFO: user-entries, user-commands."""

import os
import logging
from arc.resolve import DIR_PATH, TerminalFormatting

sy = TerminalFormatting.SYMBOL


class MainLogConfig:
    """Log configuration class."""
    def __init__(self):
        logging.basicConfig(
            filename=self.log_path,
            filemode='a',
            level=self.log_level,
            format=f'{sy[4] * 3} %(asctime)s:%(levelname)s%(message)s',
            datefmt='%Y-%m-%d__%I:%M:%S__%p'
        )
        self.logger = logging.getLogger(__name__)


class DebugLog(MainLogConfig):
    """Debugging."""
    log_path = os.path.join(DIR_PATH, 'debug.log')
    log_level = logging.DEBUG

    def __init__(self):
        super().__init__()

    def log_exception(self):
        # Module-level logger
        self.logger.debug(
            '\n' + 'Exception occured:',
            exc_info=True
        )

        self.logging.debug('\n')


class InfoLog(MainLogConfig):
    """Logging nicely formatted user-entries."""
    log_path = os.path.join(DIR_PATH, 'history.log')
    log_level = logging.INFO

    def __init__(self):
        super().__init__()

    def log_entry(self, filled_pattern):
        """Single-input blueprint:
        CMD: create/add/edit/remove
        GROUP: group name
        TASK: task description"""

        # Log generating pattern
        # pe = Pattern entry
        pe = (f'\n{sy[5] * 33}' +
              f'\n{sy[4]} CMD: %s' +
              f'\n{sy[4]} GROUP: %s' +
              f'\n{sy[4]} TASK: %s' +
              f'\n{sy[5] * 33}\n')

        self.logger.info(pe % filled_pattern)

    def log_entries(self, filled_pattern):
        """Multi-input blueprint:
        CMD: archive/purge
        GROUP: group
        TASKS LIST:
        n1,
        n2,
        n3..."""

        # First nested tuple: cmd & group
        REPL = (filled_pattern[0][0], filled_pattern[0][1])

        # Second nested tuple: tasks list
        def gen_multi_str(i=filled_pattern[1]):
            # Return row by row list of tasks
            return '\n    '.join(i)

        # Log generating pattern
        # pe = Pattern entries
        pe = (f'\n{sy[5] * 33}' +
              f'\n{sy[4]} CMD: %s' +
              f'\n{sy[4]} GROUP: %s' +
              f'\n{sy[4]} TASKS LIST:\n    {gen_multi_str()}' +
              f'\n{sy[5] * 33}\n')

        self.logger.info(pe % REPL)

    def log_rename(self, filled_pattern):
        """Single-input blueprint:
        CMD: rename
        GROUP: old name -> new name"""

        # Log generating pattern
        # pe = Pattern entry
        pe = (f'\n{sy[5] * 33}' +
              f'\n{sy[4]} CMD: %s' +
              f'\n{sy[4]} GROUP: %s' +
              f'\n{sy[5] * 33}\n')

        self.logger.info(pe % filled_pattern)
