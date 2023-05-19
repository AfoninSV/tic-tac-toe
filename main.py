import tkinter as tk
from itertools import count


class Player:
    """
    A class to represent a player.
    """
    def __init__(self, mark: str):
        """
        Player object constructor
        """
        self._name = str
        self.mark = mark
        self._is_actor = False

    @property
    def name(self):
        """Getter for name"""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name"""
        self._name = value

    @property
    def is_actor(self):
        """Getter for is_actor"""
        return self._is_actor

    @is_actor.setter
    def is_actor(self, value):
        """Setter for is_actor"""
        self._is_actor = value


class Cell(tk.Button):
    """
    A class to represent a cell.
    """
    _ids = count()

    def __init__(self, *args, **kwargs):
        """Cell object constructor"""
        self.id = next(self._ids)
        super().__init__(*args, **kwargs)
        self.is_changed = False


class StartWindow(tk.Frame):
    """
    A class to represent the Start Window
    """
    def __init__(self, master: tk.Frame, controller):
        """StartWindow object constructor"""
        super().__init__(master)

        self.p1_text, self.p1_entry = self.create_label_entry('Nickname of X (first):', 'Enter nickname...')
        self.p2_text, self.p2_entry = self.create_label_entry('Nickname of O (second):', 'Enter nickname...')

        self.confirm_btn = tk.Button(self, text='START', width=18,
                                     command=lambda: [controller.board_raise(),
                                                      controller.set_names(*self.get_names()),
                                                      controller.board_window.turn_label.configure(
                                                          text=f'Turn: {self.p1_entry.get()}'
                                                      )])

        self.position_elements()
        self.grid(row=0, column=0, sticky='nesw')

    def create_label_entry(self, text, entry_text):
        """Helper method to create a label and entry"""
        label = tk.Label(self, text=text)
        entry = tk.Entry(self, width=21)
        entry.insert(0, entry_text)
        return label, entry

    def position_elements(self):
        """Helper method to position elements"""
        self.p1_text.grid(row=1, column=0, padx=(90, 0), pady=(100, 0), sticky='w')
        self.p2_text.grid(row=3, column=0, padx=(90, 0), sticky='w')
        self.p1_entry.grid(row=2, column=0, padx=(90, 0), sticky='w')
        self.p2_entry.grid(row=4, column=0, padx=(90, 0), sticky='w')
        self.confirm_btn.grid(row=5, column=0, padx=(90, 0), sticky='w')

    def get_names(self):
        """Get player names from the entries"""
        return self.p1_entry.get(), self.p2_entry.get()


class BoardWindow(tk.Frame):
    """
    A class to represent the Board Window
    """
    def __init__(self, master: tk.Frame, controller):
        """BoardWindow object constructor"""
        super().__init__(master)

        self.n = 3  # board cells quantity
        self.player_1 = Player('X')
        self.player_2 = Player('O')
        self.actor = self.player_1

        # Initializing cells on board
        self.initialize_board()

        # Turn label indicator
        self.turn_label = tk.Label(self)
        self.turn_label.grid(row=4, column=1, columnspan=3)

        # BACK button on board
        self.back_btn = tk.Button(self, text='BACK', width=40,
                                  command=lambda: controller.start_raise(self))
        self.back_btn.grid(row=5, column=1, columnspan=3)

        self.grid(row=0, column=0)

    def initialize_board(self):
        """Method to initialize the game board"""
        self.coords = dict()  # {(x, y): Cell}
        self.buttons = list()
        self.used_buttons = list()
        for i_row in range(1, self.n + 1):
            for i_col in range(1, self.n + 1):
                btn = Cell(self, text='_', bd=5, width="10", height="5")
                btn.configure(command=lambda b=btn: self.click(b))
                btn.grid(row=i_row, column=i_col)
                self.buttons.append(btn)
                self.coords[(i_col, i_row)] = btn

    def click(self, btn: Cell):
        """Handle click event on a cell."""
        if btn.is_changed:
            return
        btn.is_changed = True
        btn['text'] = self.actor.mark
        btn['state'] = 'disabled'
        self.used_buttons.append(btn)
        if self.check_win():
            self.write_victory()
        else:
            self.swap_turn()

    def check_win(self):
        """Check if the game is won."""
        # Define winning conditions
        win_conditions = [
            # rows
            [(1, 1), (1, 2), (1, 3)],
            [(2, 1), (2, 2), (2, 3)],
            [(3, 1), (3, 2), (3, 3)],

            # columns
            [(1, 1), (2, 1), (3, 1)],
            [(1, 2), (2, 2), (3, 2)],
            [(1, 3), (2, 3), (3, 3)],

            # diagonals
            [(1, 1), (2, 2), (3, 3)],
            [(3, 1), (2, 2), (1, 3)],
        ]

        # For each win condition
        for condition in win_conditions:
            # If all cells in a condition are marked with the same player's mark
            if all(self.coords[coord]['text'] == self.actor.mark for coord in condition):
                # The game is won
                return True
        return False

    def write_victory(self):
        """Method to display victory message"""
        self.turn_label.configure(text=f'{self.actor.name} won!')
        for btn in self.buttons:
            if not btn.is_changed:
                btn['state'] = 'disabled'

    def swap_turn(self):
        """Method to swap turns between players"""
        self.actor.is_actor = False
        self.actor = self.player_2 if self.actor == self.player_1 else self.player_1
        self.actor.is_actor = True
        self.turn_label.configure(text=f'Turn: {self.actor.name}')


class VictoryWindow(tk.Frame):
    """
    A class to represent the Victory Window
    """
    def __init__(self, player: Player):
        """VictoryWindow object constructor"""
        super().__init__()
        victory_label = tk.Label(self, text=f'{player.name} won!')
        self.grid(row=0, column=2)


class MainWindow:
    """
    A class to represent the Main Window
    """
    def __init__(self, master: tk.Tk):
        """MainWindow object constructor"""
        master.title('Tic Tac Toe')
        self.main_frame = tk.Frame(master)
        self.main_frame.grid()

        self.board_window = BoardWindow(self.main_frame, self)
        self.start_window = StartWindow(self.main_frame, self)

    def start_raise(self, window_link: BoardWindow):
        """Raise the Start Window"""
        window_link.destroy()
        self.start_window.tkraise()

    def board_raise(self):
        """Raise the Board Window"""
        self.board_window = BoardWindow(self.main_frame, self)
        self.board_window.player_1.is_actor = True
        self.board_window.tkraise()

    def set_names(self, name1: str, name2: str):
        """Set player names"""
        self.board_window.player_1.name = name1
        self.board_window.player_2.name = name2


root = tk.Tk()
root.resizable(False, False)
main_window = MainWindow(root)
root.mainloop()
