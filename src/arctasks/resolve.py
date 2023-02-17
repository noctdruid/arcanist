"""Resolving common problems and providing resources."""

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
    def term_initialize(self):
        """Check sizes and ansi support."""
        if (TerminalFormatting().shell_allowed() and self._term_checkout()):
            return '__ansi__'
        if not TerminalFormatting().shell_allowed():
            sys.exit('error: terminal width or lines less than 80x20')
        return None

    def _term_checkout(self) -> bool:
        """List of tested-terminals that support ansi escape seq."""
        your_term = os.getenv('TERM')
        supp_term = [
            'xterm', 'xterm-16color', 'xterm-256color',
        ]  # if you have different terminal that supports ansi escape seq
        # ... you can add it here in supp_term list

        # Return True if your terminal matches supported list
        return bool(your_term in supp_term)

    def dir_check(self, path=DIR_PATH) -> bool:
        """Checking directory."""
        dir_exist = os.path.isdir(path)

        if dir_exist:
            dir_perm = (os.access(path, os.R_OK) + os.access(path, os.W_OK))
            if dir_perm:
                return True
            sys.exit(f'check if directory has right permissions:\n{path}')

        elif not dir_exist:
            # Create directory
            os.mkdir(path)
            json_object = json.dumps({'all': []}, indent=4)
            arc_store = os.path.join(DIR_PATH, 'arc.json')
            archive_store = os.path.join(DIR_PATH, 'archive.json')

            with open(arc_store, 'w', encoding='utf-8') as newfile:
                newfile.write(json_object)
                newfile.close()

            with open(archive_store, 'w', encoding='utf-8') as newfile:
                newfile.write(json_object)
                newfile.close()

            return True

        # Unknown directory corruption
        return False


class TerminalFormatting:
    """Class for terminal properties, formatting projections.
    :attr term_pads: four left and four right chars space,
    :attr shell_width: for comfortable usage-experience,
    :attr shell_lines: for comfortable usage-experience."""
    SYMBOL = ('☐', '…', '➤', '✔', '🞂', '#', '█')
    generic_chars = 36  # Minimal number of generic characters
    user_shell_width = shutil.get_terminal_size().columns
    user_shell_lines = shutil.get_terminal_size().lines

    def __init__(self):
        self.term_pads = 8
        self.shell_width = 80
        self.shell_lines = 20

    def shell_allowed(self) -> bool:
        """Check if term-width >= 80 and term-lines >= 20."""
        check_width = self.shell_width <= self.user_shell_width
        check_lines = self.shell_lines <= self.user_shell_lines
        return bool(check_width and check_lines)

    def add_space(self, digit) -> str:
        """Add space in front of single digit id_key.
        :return: str type formatted digit (id_key): ' 1' or '11'."""
        if digit < 10:
            return ' ' + str(digit)
        return str(digit)

    def measure_task_desc(self, input_string) -> int:
        """Measure maximum task description length before it
        get across new line.
        :return: int type difference between:
            - program allowed task description length
            - user-input task description length"""
        string_length = len(input_string)
        max_desc_length = (
            self.user_shell_width - self.generic_chars - self.term_pads - 1
        )
        return max_desc_length - string_length
