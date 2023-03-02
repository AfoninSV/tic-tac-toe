import tkinter as tk
from itertools import count


class Player:
    def __init__(self, mark: str):
        self.name = str
        self.mark = mark
        self.is_actor = False

    def set_name(self, name_str):
        self.name = name_str


class Cell(tk.Button):
    _ids = count()

    def __init__(self, *args, **kwargs):
        self.id = next(self._ids)
        super().__init__(*args, **kwargs)
        self.is_changed = False


class StartWindow(tk.Frame):

    def __init__(self, master: tk.Frame, controller):
        super().__init__(master)

        # input spot
        self.p1_text = tk.Label(self, text='Nickname of X (first):')
        self.p2_text = tk.Label(self, text='Nickname of O (second):')
        self.p1_entry = tk.Entry(self, width=21)
        self.p2_entry = tk.Entry(self, width=21)
        self.p1_entry.insert(0, 'Enter nickname...')
        self.p2_entry.insert(0, 'Enter nickname...')
        # confirm button
        self.confirm_btn = tk.Button(self, text='START', width=19,
                                     command=lambda: [controller.board_raise(),
                                                      controller.set_names(*self.get_names()),
                                                      controller.board_window.turn_label.configure(
                                                          text=self.p1_entry.get()
                                                      )])
        # positioning
        self.p1_text.grid(row=1, column=0, padx=100, pady=(100, 0))
        self.p2_text.grid(row=3, column=0)
        self.p1_entry.grid(row=2, column=0)
        self.p2_entry.grid(row=4, column=0)
        self.confirm_btn.grid(row=5, column=0)

        self.grid(row=0, column=0, sticky='nesw')

    def get_names(self):
        return self.p1_entry.get(), self.p2_entry.get()


class BoardWindow(tk.Frame):
    def __init__(self, master: tk.Frame, controller):
        super().__init__(master)

        self.n = 3  # board cells qty
        self.player_1 = Player('X')
        self.player_2 = Player('O')
        self.actor = self.player_1

        # initializing cells on board
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

        # turn label indicator
        self.turn_label = tk.Label(self)
        self.turn_label.grid(row=4, column=1, columnspan=3)
        # BACK button on board
        self.back_btn = tk.Button(self, text='BACK', width=40)
        self.back_btn.grid(row=5, column=1, columnspan=3)
        self.back_btn.configure(command=lambda: controller.start_raise(self))

        self.grid(row=0, column=0)

    def write_victory(self):
        self.turn_label.configure(text=f'{self.actor.name} won!')

    def win_check(self):
        if len(self.used_buttons) == (self.n * self.n):
            self.write_victory()
            return True
        # check horizontals
        for y in range(1, self.n + 1):
            for x in range(1, self.n + 1):
                cell = self.coords.get((x, y))
                cell_mark = cell['text']
                if cell_mark != self.actor.mark:
                    break
            else:
                self.write_victory()
                return True
        # check verticals
        for x in range(1, self.n + 1):
            y = count(start=1)
            while cell := self.coords.get((x, next(y))):
                if cell['text'] != self.actor.mark:
                    break
            else:
                self.write_victory()
                return True

        # check diagonal \
        for x in range(1, self.n + 1):
            cell = self.coords.get((x, x))
            cell_mark = cell['text']
            if cell_mark != self.actor.mark:
                break
        else:
            self.write_victory()
            return True
        # check diagonal /
        for x in range(self.n, 0, -1):
            cell = self.coords.get((x, self.n - (x - 1)))
            cell_mark = cell['text']
            if cell_mark != self.actor.mark:
                break
        else:
            self.write_victory()
            return True

    def click(self, button: Cell):
        if not button.is_changed:
            button.configure(text=self.actor.mark)
            button.is_changed = True
            self.used_buttons.append(button)
            if self.win_check():
                return
            self.swap_turn()

    def swap_turn(self):
        if self.player_1.is_actor:
            self.player_1.is_actor = False
            self.player_2.is_actor = True
            self.actor = self.player_2
        else:
            self.player_2.is_actor = False
            self.player_1.is_actor = True
            self.actor = self.player_1
        self.turn_label.configure(text=f'Turn: {self.actor.name}')


class VictoryWindow(tk.Frame):
    def __init__(self, player: Player):
        super().__init__()
        victory_label = tk.Label(self, text=f'{player.name} won!')
        self.grid(row=0, column=2)


class MainWindow:
    def __init__(self, master: tk.Tk):
        master.title('Tic Tac Toe')
        self.main_frame = tk.Frame(master)
        self.main_frame.grid()

        self.board_window = BoardWindow(self.main_frame, self)
        self.start_window = StartWindow(self.main_frame, self)

    def start_raise(self, window_link: BoardWindow):
        window_link.destroy()
        self.start_window.tkraise()

    def board_raise(self):
        self.board_window = BoardWindow(self.main_frame, self)
        self.board_window.player_1.is_actor = True
        self.board_window.tkraise()

    def set_names(self, name1: str, name2: str):
        self.board_window.player_1.set_name(name1)
        self.board_window.player_2.set_name(name2)

    def write_turn(self, turn_name):
        self.board_window.turn_label.configure(text=f'Turn: {self.board_window.actor.name}')


root = tk.Tk()
root.resizable(False, False)
main_window = MainWindow(root)
root.mainloop()
