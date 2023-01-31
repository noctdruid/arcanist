import os
import sys
import json
import shutil
from datetime import datetime

# determinate path: /home/$USER/.arc-tasks/
PATH = os.path.expanduser(os.getenv('HOME'))
DIR_PATH = os.path.join(PATH, '.arc-tasks')

# datetime format example: 20-JAN-2023
now = datetime.now().strftime("%d-%b-%Y").upper()


class InitCheckout:
    """Get $TERM and return ansi format support.
    Check if directory exist and have right permissions."""
    def term_initialize(self) -> str:
        if (TerminalFormatting().shell_allowed() and self._term_checkout()):
            return '__ansi__'

        elif TerminalFormatting().shell_allowed():
            return

        else:
            sys.exit('error: terminal width or lines less than 80x20')

    def _term_checkout(self) -> bool:
        """List of tested-terminals that support ansi escape seq."""
        your_term = os.getenv('TERM')
        supp_term = [
            'xterm', 'xterm-16color', 'xterm-256color',
        ]  # if you have different terminal that supports ansi escape seq
        # ... you can add it here in supp_term list

        if your_term in supp_term:
            return True
        else:
            return False

    def dir_check(self, path=DIR_PATH) -> bool:
        """Checking directory."""
        dir_exist = os.path.isdir(path)

        if dir_exist:
            dir_perm = (os.access(path, os.R_OK) + os.access(path, os.W_OK))
            if dir_perm:
                return True
            else:
                sys.exit(f'check if directory has right permissions:\n{path}')

        elif not dir_exist:
            # Create directory
            os.mkdir(path)
            json_object = json.dumps({'all': []}, indent=4)
            arc_store = os.path.join(DIR_PATH, 'arc.json')
            archive_store = os.path.join(DIR_PATH, 'archive.json')

            with open(arc_store, 'w') as newfile:
                newfile.write(json_object)
                newfile.close()

            with open(archive_store, 'w') as newfile:
                newfile.write(json_object)
                newfile.close()

            return True

        else:
            # Possible system corruptions
            return False


class TerminalFormatting:

    SYMBOL = ('☐', '…', '➤', '✔', '🞂', '#', '█')
    MIN_GEN_CHARS = 36  # minimal number of generic characters
    user_shell_width = shutil.get_terminal_size().columns
    user_shell_lines = shutil.get_terminal_size().lines

    def __init__(self):
        """Class for terminal properties, formatting projections.
        :attr SHELL_PADS: four left and four right chars space,
        :attr MIN_SHELL_ALLOWED: for comfortable usage-experience."""
        self.SHELL_PADS = 8
        self.MIN_SHELL_ALLOWED = 80
        self.MIN_SHELL_LINES = 20

    def shell_allowed(self) -> bool:
        """Check if term-width >= 80 and term-lines >= 20."""
        if (
            (self.MIN_SHELL_ALLOWED <= self.user_shell_width) and
            (self.MIN_SHELL_LINES <= self.user_shell_lines)
        ):
            return True

    def add_space(self, digit) -> str:
        """Add space in front of single digit id_key.
        :return: str type formatted digit (id_key): ' 1' or '11'."""
        if digit < 10:
            return ' ' + str(digit)
        else:
            return str(digit)

    def measure_task_desc(self, input_string) -> int:
        """Measure maximum task description length before it
        get across new line.
        :return: int type difference between:
            - program allowed task description length
            - user-input task description length"""
        string_length = len(input_string)
        max_desc_length = (
            self.user_shell_width - self.MIN_GEN_CHARS - self.SHELL_PADS - 1
        )
        return max_desc_length - string_length
