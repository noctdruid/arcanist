import os
import sys
import shutil
from datetime import datetime

# determinate path: /home/$USER/.arc-tasks/
PATH = os.path.expanduser('~')
DIR_PATH = os.path.join(PATH, '.arc-tasks')

# datetime format example: 20-JAN-2023
now = datetime.now().strftime("%d-%b-%Y").upper()


class InitCheckout:
    """ Get $TERM and return ansi/filter format.
    Check if directory exist and have right permissions. """
    def term_initialize(self) -> str:
        if (TerminalFormatting().shell_allowed() and self._term_checkout()):
            return '__ansi__'

        elif (self._dir_check() and TerminalFormatting().shell_allowed()):
            return '__filter__'

    def _term_checkout(self) -> bool:
        """ List of tested-terminals that support ansi escape seq """
        your_term = os.getenv('TERM')
        supp_term = [
            'xterm', 'xterm-16color', 'xterm-256color', 'iTerm2',
        ]  # more terminal emulators will be added

        if your_term in supp_term:
            return True
        else:
            return False

    def dir_check(self, path=DIR_PATH) -> bool:
        """ Method for checking directory """
        dir_exist = os.path.isdir(path)

        if dir_exist:
            dir_perm = (os.access(path, os.R_OK) + os.access(path, os.W_OK))
            if dir_perm:
                return True
            else:
                print(f'check if directory has right permissions:\n{path}')
                sys.exit(1)

        elif not dir_exist:
            # create directory
            os.mkdir(path)
            return True

        else:
            return False


class TerminalFormatting:
    """ Class for terminal properties, formatting projections """

    SYMBOL = ('☐', '…', '➤', '✔', '🞂', '#', '█')
    MIN_GEN_CHARS = 36  # minimal number of generic characters
    user_shell_width = shutil.get_terminal_size().columns

    def __init__(self):
        self.SHELL_PADS = 8  # left-right shell padding
        self.MIN_SHELL_ALLOWED = 72  # req: minimal columns width 72

    def shell_allowed(self) -> bool:
        if self.MIN_SHELL_ALLOWED <= self.user_shell_width:
            return True

    def add_space(self, digit) -> str:
        # add space in front of single digit id_key
        if digit < 10:
            return ' ' + str(digit)
        else:
            return str(digit)

    def measure_task_desc(self, input_string) -> int:
        # return maximum task description length
        string_length = len(input_string)
        max_desc_length = (
            self.user_shell_width - self.MIN_GEN_CHARS - self.SHELL_PADS - 1
        )
        return max_desc_length - string_length
