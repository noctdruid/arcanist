"""Two-levels logging."""

import os
import logging
from arctasks.resolve import DIR_PATH, TerminalFormatting

f_symb = TerminalFormatting.SYMBOL


class MainLogConfig:
    """Log configuration class."""
    def __init__(self):
        logging.basicConfig(
            filename=self.log_path,
            filemode='a',
            level=self.log_level,
            format=f'{f_symb[4] * 3} %(asctime)s:%(levelname)s%(message)s',
            datefmt='%Y-%m-%d__%I:%M:%S__%p'
        )
        self.logger = logging.getLogger(__name__)


class DebugLog(MainLogConfig):
    """Debugging."""
    log_path = os.path.join(DIR_PATH, 'debug.log')
    log_level = logging.DEBUG

    def log_exception(self):
        """Logging exception."""
        self.logger.debug('\nException occured:', exc_info=True)


class InfoLog(MainLogConfig):
    """Logging nicely formatted user-entries."""
    log_path = os.path.join(DIR_PATH, 'history.log')
    log_level = logging.INFO

    def log_entry(self, filled_pattern):
        """Log for create/add/edit/remove commands."""

        # Log generating pattern
        pattern_entry = (f'\n{f_symb[5] * 33}' +
                         f'\n{f_symb[4]} CMD: %s' +
                         f'\n{f_symb[4]} GROUP: %s' +
                         f'\n{f_symb[4]} TASK: %s' +
                         f'\n{f_symb[5] * 33}\n')

        self.logger.info(pattern_entry % filled_pattern)

    def log_entries(self, filled_pattern):
        """Log for archive/purge commands."""

        # Pattern generating first part
        pattern_parts = (filled_pattern[0][0], filled_pattern[0][1])

        # Pattern generating second part
        def _gen_multi_str(i=filled_pattern[1]):
            """Return multi-line string."""
            return '\n    '.join(i)

        # Log generating pattern
        pattern_entry = (f'\n{f_symb[5] * 33}' +
                         f'\n{f_symb[4]} CMD: %s' +
                         f'\n{f_symb[4]} GROUP: %s' +
                         f'\n{f_symb[4]} TASKS LIST:\n    {_gen_multi_str()}' +
                         f'\n{f_symb[5] * 33}\n')

        self.logger.info(pattern_entry % pattern_parts)

    def log_rename(self, filled_pattern):
        """Log for group rename command."""

        # Log generating pattern
        pattern_entry = (f'\n{f_symb[5] * 33}' +
                         f'\n{f_symb[4]} CMD: %s' +
                         f'\n{f_symb[4]} GROUP: %s' +
                         f'\n{f_symb[5] * 33}\n')

        self.logger.info(pattern_entry % filled_pattern)
