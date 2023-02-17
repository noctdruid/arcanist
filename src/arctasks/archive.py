"""Building textual user-interface for tasks custom archives."""

import curses
from arctasks.resolve import now
from arctasks.doc import MENU as menu


class Archive:
    """Very simple presentation of archived tasks."""
    def __init__(self):
        self.done = '✔'
        self.not_done = '☐'

    def transform(self, group, archive_name=None) -> dict:
        """Preparing group and tasks for json store.
        :param group: dict containing group and tasks,
        :return: formatted dict containing group and tasks."""
        name = archive_name
        group_dict = {'date': now, 'name': name, 'tasks': []}

        # get task variables
        for task in group['tasks']:
            task_status = bool(task['status'] == 'done')
            task_name = task['desc']
            task_dict = {'completion': task_status, 'name': task_name}

            # insert task object in group object
            group_dict['tasks'].append(task_dict)

        return group_dict

    def stack(self, archive) -> str:
        """Create string from archive.json file.
        :param archive: load from json file
        :return: multi-line string"""
        task_archive = """"""
        groups = archive['all']

        # Formatting group and task lines
        for group in groups:
            date = group['date']
            group_name = group['name']

            # Formatting group lines
            if group is not groups[0]:
                task_archive = task_archive + f'\n [{date}] » {group_name}'
            else:
                task_archive = task_archive + f' [{date}] » {group_name}'

            for task in group['tasks']:
                # Formatting task lines
                if task['completion'] is True:
                    task_symb = self.done
                    task_name = task['name']
                else:
                    task_symb = self.not_done
                    task_name = task['name']

                if group is groups[-1] and task is group['tasks'][-1]:
                    task_archive = task_archive + f'\n {task_symb} {task_name}'
                elif task is group['tasks'][-1]:
                    task_archive = (
                        task_archive + f'\n {task_symb} {task_name}\n'
                    )
                else:
                    task_archive = task_archive + f'\n {task_symb} {task_name}'

        return task_archive


class ArchiveUI:
    """ArchiveUI is class for building curses screen,
    displaying archive.json and adding navigation functionality.
    :param archive: mod archive.json file input."""
    curr_page = 1
    cut_lines = 0

    def __init__(self, archive):
        # Start curses and set instance attributes
        self.init_curses()
        self.max_lines = curses.LINES
        self.max_cols = curses.COLS
        self.archive = archive
        self.split_excessed()
        self.max_page = self.paging()
        self.parse_archive = self.archive

    def init_curses(self):
        """Initialize curses behaviour."""
        self.window = curses.initscr()  # Initialize screen
        self.window.keypad(True)  # Enable keypad

        curses.curs_set(0)  # Disable cursor
        curses.noecho()  # No screen echoes
        curses.cbreak()  # Enter cbreak mode

        # Start terminal color and Initialize pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)

    def run(self):
        """Starting curses."""
        try:
            self.input_stream()  # user-inputs
        except KeyboardInterrupt:
            pass
        except curses.error:
            pass
        finally:
            curses.curs_set(1)  # Set back cursor
            curses.echo()  # Set back echoes
            curses.nocbreak()  # Turn off cbreak mode
            self.window.keypad(False)  # Disable keypad
            curses.endwin()  # Quit window

    def input_stream(self):
        """Program control using while loop and user actions."""
        move_down = 1
        move_up = -1

        # Running until user interrupts
        while True:
            self.display()
            key_ch = self.window.getch()
            if key_ch == curses.KEY_DOWN:
                # One line down
                self.line_nav(move_down)

            elif key_ch == curses.KEY_UP:
                # One line up
                self.line_nav(move_up)

            elif key_ch == curses.KEY_NPAGE:
                # Next page (PgDn)
                if self.max_page != 1:
                    self.page_nav(move_down)

            elif key_ch == curses.KEY_PPAGE:
                # Previous page (PgUp)
                if self.max_page != 1:
                    self.page_nav(move_up)

            elif key_ch == curses.KEY_HOME:
                # First page
                if self.curr_page != 1:
                    self.home_nav()

            elif key_ch == curses.KEY_END:
                # Last page
                if self.curr_page != self.max_page:
                    self.end_nav()

            elif (key_ch == ord('q') or key_ch == ord('Q')):
                # Quit program
                break

    def archive_lines(self):
        """Determinate how many KEY_DOWN strokes left."""
        # Every key stroke cuts down one line, after it reaches
        # zero result: in line_nav method it subtracts additional cuts.
        lines = self.archive.split('\n')
        return len(lines) - self.max_lines + 4

    def line_nav(self, direction):
        """Lines navigation.
        :param direction: direct move up or down"""
        self.cut_lines += direction
        archive = self.archive
        lines = archive.split('\n')

        # Block line exceeding or move
        if self.cut_lines == -1:
            self.cut_lines = 0
        elif self.cut_lines > self.archive_lines():
            self.cut_lines -= 1
        else:
            self.parse_archive = '\n'.join(lines[self.cut_lines:])

        # Calculate current page
        quotient = (self.max_lines - 4 + self.cut_lines) / (self.max_lines - 4)
        if float(quotient) == int(quotient):
            self.curr_page = int(quotient)
        else:
            self.curr_page = int(quotient) + 1

    def page_nav(self, direction):
        """Page navigation.
        :param direction: direct move up or down"""
        self.curr_page += direction

        # Block page exceeding
        if self.curr_page < 1:
            self.curr_page = 1
        elif self.curr_page > self.max_page:
            self.curr_page -= 1

        # Split lines and calculate how many lines
        # should be cut from beginning
        lines = self.archive.split('\n')
        self.cut_lines = (self.max_lines - 4) * (self.curr_page - 1)

        # Next or previous page
        if self.curr_page == self.max_page:
            self.end_nav()
        else:
            self.parse_archive = '\n'.join(lines[self.cut_lines:])

    def paging(self):
        """Calculate total pages."""
        archive = self.archive
        lines = archive.split('\n')
        quotient = len(lines) / (self.max_lines - 4)

        if quotient <= 1:
            return 1
        if float(quotient) == int(quotient):
            return int(quotient)
        return int(quotient) + 1

    def home_nav(self):
        """Sets lines to initial state."""
        self.cut_lines = 0
        self.curr_page = 1
        self.parse_archive = self.archive

    def end_nav(self):
        """Sets lines to match last archive lines."""
        self.cut_lines = self.archive_lines()
        self.curr_page = self.max_page
        lines = self.archive.split('\n')
        self.parse_archive = '\n'.join(lines[4 - self.max_lines:])

    def split_excessed(self):
        """Splitting multi-line tasks."""
        lines = self.archive.split('\n')
        new_lines = []
        for line in lines:
            if len(line) > self.max_cols:
                parts = self.parse_line(line)
                for part in parts:
                    new_lines.append(part)
            else:
                new_lines.append(line)
        self.archive = '\n'.join(new_lines)

    def parse_line(self, multi_line) -> list:
        """Parsing task entries that are longer than
        terminal columns-width.
        :return: list with multi-line task parts"""
        parts = []
        row_words = []
        words = multi_line.split(' ')

        def join_lines():
            line_generator = ' '.join(row_words)
            return line_generator

        for word in words:
            row_length = len(join_lines()) + len(word) + 1
            if row_length <= self.max_cols and word is words[-1]:
                row_words.append(word)
                parts.append(join_lines())

            elif row_length > self.max_cols and word is words[-1]:
                parts.append(join_lines())
                parts.append(' ' + word)

            elif row_length == self.max_cols:
                parts.append(join_lines())
                row_words = ['']

            elif row_length <= self.max_cols:
                row_words.append(word)

            elif row_length > self.max_cols:
                parts.append(join_lines())
                row_words = [' ' + word]

        return parts

    def gen_view(self) -> str:
        """Generating display lines."""
        lines = self.parse_archive.split('\n')
        lines = lines[:self.max_lines - 4]
        lines = '\n'.join(lines)
        return lines

    def display(self):
        """Display an archive in the window."""
        self.window.clear()
        self.window.bkgd(' ', curses.color_pair(1))
        last_line = self.max_lines - 1
        pads = (self.max_cols - len(menu)) // 2
        view = self.gen_view()

        header_pads = (self.max_cols - 15) // 2 * ' '
        header = f'{header_pads}»»» archive «««{header_pads}'
        if len(header) != self.max_cols:
            header = f'{header} '

        self.window.addstr(0, 0, header, curses.color_pair(2))
        self.window.addstr(2, 0, view, curses.color_pair(1))
        self.window.addstr(
            last_line, pads, (menu % (self.curr_page, self.max_page)),
            curses.color_pair(2)
        )
        self.window.refresh()
