from arc.resolve import InitCheckout, TerminalFormatting


class Board:

    def __init__(self):
        """Terminal objectives presentation.
        :var checkout: $TERM property,
        if checkout '__ansi__' then use:
        ansi escape seq formatting:
        :attr n: ansi normal escape seq,
        :attr u: ansi underline escape seq,
        :attr i: ansi inverted escape seq,
        :attr c: ansi crossed escape seq.
        else - don't use.
        :attr s: single space
        :attr t: four spaces (tab)
        :attr sq, pending, inprog, arrow, done: iso chars,
        :attr user_shell: get size of char columns width,
        :attr generic: generic chars always on same position."""

        checkout = InitCheckout().term_initialize()
        if checkout == '__ansi__':
            self.n = '\033[0m'  # ansi normal
            self.u = '\033[4m'  # ansi underline
            self.i = '\033[7m'  # ansi inverted
            self.c = '\033[9m'  # ansi crossed
        else:
            self.n = ''
            self.u = ''
            self.i = ''
            self.c = ''

        self.s = ' '
        self.t = '    '

        self.sq = TerminalFormatting.SYMBOL[6]
        self.user_shell = TerminalFormatting.user_shell_width
        self.generic = TerminalFormatting.MIN_GEN_CHARS

        self.pending = TerminalFormatting.SYMBOL[0]
        self.inprog = TerminalFormatting.SYMBOL[1]
        self.arrow = TerminalFormatting.SYMBOL[2]
        self.done = TerminalFormatting.SYMBOL[3]

    def group_formatting(self, id_key, name, done, total):
        """Group id_key, group name, minimal statistic [DONE/TOTAL]."""
        stats = f'[{done}/{total}]'
        return f'\n{self.t}#{id_key} {name} {stats}'

    def column_formatting(self):
        """Ansi escape seq inverted column categories: id, start, end, task."""
        first_part = f"{self.s}id{self.s*9}start{self.s*10}end{self.s*6}"

        blank = (((self.user_shell - self.generic - 8) // 2) - 4) * ' '
        left = (self.user_shell - 12 - self.generic - len(blank)) * ' '

        # return: TUI-like column annotations
        return f"{self.t}{self.i}{first_part}{blank}task{left}{self.n}"

    def task_formatting(self, *args):
        """Process of determining task formatting properties."""
        # formatting: task key_id
        f_id = TerminalFormatting().add_space(args[0])

        # formatting: task description
        task_length_fit = TerminalFormatting().measure_task_desc(args[4])
        if task_length_fit < 0:
            # dots_added = max_length - 3
            f_desc = f'{args[4][:task_length_fit - 3]}...'
        else:
            f_desc = args[4]

        # formatting: status-dependent
        if args[1] == 'pending':
            symb = self.pending
        elif args[1] == 'inprog':
            symb = self.inprog
            if task_length_fit <= 1:
                f_desc = f'{self.arrow} {args[4][:task_length_fit - 5]}...'
            else:
                f_desc = f'{self.arrow} {args[4]}'
        else:
            symb = self.done
            f_desc = f'{self.c}{f_desc}{self.n}'

        # return: formatted-task ready for presentation
        return '{0}{1} {2} {3} {4} {5} {6} {7} {8} {9}'.format(
            self.t, f_id, self.sq, symb, self.sq, args[2], self.sq,
            args[3], self.sq, f_desc
        )

    def _statistics(self, done, doing, not_done):
        """Method for printing overall statistics."""
        # calculation of statistics, formatting
        total = done + doing + not_done
        quotient = done / total
        perc = quotient * 100

        first_row = f'[{done}/{total}] - {round(perc)}% of all tasks complete.'
        second_row = f'{self.u}[{done}] DONE{self.n}' + ' • ' + \
            f'{self.u}[{doing}] IN-PROGRESS{self.n}' + ' • ' + \
            f'{self.u}[{not_done}] PENDING{self.n}'

        # return: overall completion status presentation
        return [first_row, second_row]
