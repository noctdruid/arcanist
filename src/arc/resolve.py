import os
import sys
import shutil
from datetime import datetime

# determinate path: /home/$USER/.arc-tasks/
PATH = os.path.expanduser('~')
DIR_PATH = os.path.join(PATH, '.arc-tasks')

# datetime format example: 20-JAN-2023
now = datetime.now().strftime("%d-%b-%Y").upper()


# resolve possible corruptions of storing directory
def dir_check():
    dir_exist = os.path.isdir(DIR_PATH)

    if dir_exist:
        directory_permission = os.access(DIR_PATH, os.W_OK)
        if directory_permission:
            return True
        else:
            print('check if directory has rwx permissions: ~/.clt')
            sys.exit(1)

    elif not dir_exist:
        # create directory
        os.mkdir(DIR_PATH)
        return True

    else:
        return False


class ShellFormatting:
    """ Class for shell metadata, formatting projections """

    SYMBOL = ('☐', '…', '➤', '✔', '🞂', '#', '█')
    MIN_GEN_CHARS = 36  # minimal number of generic characters
    user_shell_width = shutil.get_terminal_size().columns

    def __init__(self):
        self.SHELL_PADS = 8  # left-right shell padding
        self.MIN_SHELL_ALLOWED = 72  # req: minimal user-shell width

    def shell_allowed(self):
        if self.MIN_SHELL_ALLOWED <= self.user_shell_width:
            return True

    def add_space(self, digit):
        # add space in front of single digit id_key
        if digit < 10:
            return ' ' + str(digit)
        else:
            return str(digit)

    def measure_task_desc(self, input_string):
        # return maximum task description length
        string_length = len(input_string)
        max_desc_length = (
            self.user_shell_width - self.MIN_GEN_CHARS - self.SHELL_PADS - 1
        )
        return max_desc_length - string_length
