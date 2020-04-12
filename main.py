import tkinter as tk
from copy import deepcopy
from tkinter import messagebox

import tictactoe


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.state = tictactoe.get_state()
        self.initial_state = deepcopy(self.state)
        self.buttons = {}
        self.create_widgets()

    def create_widgets(self):
        for y, row in enumerate(self.state):
            for x, value in enumerate(row):
                btn = tk.Button(self)
                btn_text = tk.StringVar()
                btn["textvariable"] = btn_text

                if value != "#":
                    btn_text.set(value)
                    btn["state"] = "disabled"

                btn["command"] = self.get_command(btn, btn_text, x, y)
                btn["width"] = 1
                btn.grid(row=y, column=x)

                self.buttons[(x, y)] = (btn, btn_text)

        reset_btn = tk.Button(self, text="Reset", command=self.reset, width=10)
        reset_btn.grid(row=4, columnspan=3)

    def get_command(self, btn, btn_text, x, y):
        def make_move():
            btn_text.set(tictactoe.player(self.state))
            btn["state"] = "disabled"
            self.state = tictactoe.result(self.state, (x, y))

            if tictactoe.terminal(self.state):
                self.game_over()
                return

            self.opponent_plays()

        return make_move

    def opponent_plays(self):
        player = tictactoe.player(self.state)

        if player == tictactoe.PLAYER_O:
            _, action = tictactoe.min_value(self.state)
        else:
            _, action = tictactoe.max_value(self.state)

        btn, btn_text = self.buttons[action]

        btn_text.set(player)
        btn["state"] = "disabled"
        self.state = tictactoe.result(self.state, action)

        if tictactoe.terminal(self.state):
            self.game_over()

    def game_over(self):
        score = tictactoe.utility(self.state)

        if score == tictactoe.RESULT_X_WINS:
            msg = "Player x wins"
        elif score == tictactoe.RESULT_O_WINS:
            msg = "Player o wins"
        else:
            msg = "It's a draw"

        messagebox.showinfo("Game Over", msg)

        self.reset()

    def reset(self):
        self.state = self.initial_state

        for (x, y), (btn, btn_text) in self.buttons.items():
            text = self.state[y][x]
            btn_text.set("" if text == "#" else text)
            btn["state"] = "normal" if text == "#" else "disabled"


root = tk.Tk()
app = Application(master=root)
app.mainloop()
