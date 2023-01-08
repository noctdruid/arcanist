from resolve import ShellFormatting


class Board:
    """ Terminal objectives presentation """
    def __init__(self):
        self.n = '\033[0m'  # ansi normal
        self.i = '\033[7m'  # ansi inverted
        self.s = ' '  # space
        self.t = '    '  # tab

        self.sq = ShellFormatting.SYMBOL[6]
        self.user_shell = ShellFormatting.user_shell_width
        self.generic = ShellFormatting.MIN_GEN_CHARS

    def group_formatting(self, id_key, name, stats):
        # group id_key, group name, minimal statistic [DONE/TOTAL]
        return f'{self.t}#{id_key} {name} {stats}'

    def column_formatting(self):
        "Ansi escape seq inverted column categories: id, start, end, task"
        first_part = f"{self.s}id{self.s*9}start{self.s*10}end{self.s*6}"

        blank = (((self.user_shell - self.generic - 8) // 2) - 4) * ' '
        left = (self.user_shell - 12 - self.generic - len(blank)) * ' '

        return f"{self.t}{self.i}{first_part}{blank}task{left}{self.n}"

    def task_formatting(self, *args):
        # formatting: task key_id
        f_id = ShellFormatting().add_space(args[0])

        # formatting: task description
        task_length = ShellFormatting().measure_task_desc(args[4])
        if task_length < 0:
            # dots_added = max_length - 3
            f_desc = f'{args[4][:task_length - 3]}...'
        else:
            f_desc = args[4]

        return '{0}{1} {2} {3} {4} {5} {6} {7} {8} {9}'.format(
            self.t, f_id, self.sq, args[1], self.sq, args[2], self.sq,
            args[3], self.sq, f_desc
        )
