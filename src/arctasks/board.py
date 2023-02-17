"""Formatting lines and grouping for terminal view."""

from arctasks.resolve import InitCheckout, TerminalFormatting


class Board:
    """Terminal objectives presentation."""
    # Ansi escape sequences and whitespaces
    ansi = {
        'normal': '',
        'under': '',
        'invert': '',
        'cross': '',
        'space': ' ',
        'tab': '    ',
    }

    # Illustration Symbols
    utf = {
        'pending': TerminalFormatting.SYMBOL[0],
        'inprog': TerminalFormatting.SYMBOL[1],
        'arrow': TerminalFormatting.SYMBOL[2],
        'check': TerminalFormatting.SYMBOL[3],
        'square': TerminalFormatting.SYMBOL[6],
    }

    def __init__(self):
        """:var checkout: $TERM property,
        if checkout '__ansi__' then use ansi escape seq.
        :attr user_shell: get size of char columns width,
        :attr generic: generic chars always on the same position."""

        def _value_changes():
            self.ansi['normal'] = '\033[0m'  # ansi normal
            self.ansi['under'] = '\033[4m'  # ansi underline
            self.ansi['invert'] = '\033[7m'  # ansi inverted
            self.ansi['cross'] = '\033[9m'  # ansi crossed

        checkout = InitCheckout().term_initialize()
        if checkout == '__ansi__':
            # For ansi support terminal replace ansi dict values
            _value_changes()

        self.user_shell = TerminalFormatting.user_shell_width
        self.generic = TerminalFormatting.generic_chars

    def group_formatting(self, id_key, name, done, total):
        """Group id_key, group name, minimal statistic [DONE/TOTAL]."""
        stats = f'[{done}/{total}]'
        return f"\n{self.ansi['tab']}#{id_key} {name} {stats}"

    def column_formatting(self):
        """Ansi escape seq inverted column categories: id, start, end, task."""
        first_part = f"{self.ansi['space']}id{self.ansi['space']*9}" + \
            f"start{self.ansi['space']*10}end{self.ansi['space']*6}"

        blank = (((self.user_shell - self.generic - 8) // 2) - 4) * ' '
        left = (self.user_shell - 12 - self.generic - len(blank)) * ' '

        # return: inverted column categories
        return f"{self.ansi['tab']}{self.ansi['invert']}{first_part}" + \
            f"{blank}task{left}{self.ansi['normal']}"

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
            symb = self.utf['pending']
        elif args[1] == 'inprog':
            symb = self.utf['inprog']
            if task_length_fit <= 1:
                f_desc = f"{self.utf['arrow']} " + \
                    f"{args[4][:task_length_fit - 5]}..."
            else:
                f_desc = f"{self.utf['arrow']} {args[4]}"
        else:
            symb = self.utf['check']
            f_desc = f"{self.ansi['cross']}{f_desc}{self.ansi['normal']}"

        # return: formatted-task ready for presentation
        return '{0}{1} {2} {3} {4} {5} {6} {7} {8} {9}'.format(
            self.ansi['tab'], f_id, self.utf['square'], symb,
            self.utf['square'], args[2], self.utf['square'],
            args[3], self.utf['square'], f_desc
        )

    def statistics(self, done, doing, not_done):
        """Printing overall statistics."""
        # Calculation of statistics, formatting
        total = done + doing + not_done
        quotient = done / total
        perc = quotient * 100

        spot = ' • '
        first_row = f'[{done}/{total}] - {round(perc)}% of all tasks complete.'
        second_row = f"{self.ansi['under']}[{done}] " + \
            f"DONE{self.ansi['normal']}{spot}" + \
            f"{self.ansi['under']}[{doing}] " + \
            f"IN-PROGRESS{self.ansi['normal']}{spot}" + \
            f"{self.ansi['under']}[{not_done}] PENDING{self.ansi['normal']}"

        # return: overall completion status presentation
        return [first_row, second_row]
