import tkinter as tk
import random
from tkinter import messagebox
import sys

class MinesweeperGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.start_game()

    def quit_app(self):
        sys.exit()

    def start_game(self):
        self.rows = 12
        self.cols = 12
        self.mines_count = 25
        self.revealed_count = 0
        self.game_over = False
        
        self.logic_board = []
        for r in range(self.rows):
            new_row = []
            for c in range(self.cols):
                new_row.append(0)
            self.logic_board.append(new_row)
        
        self.buttons = []
        for r in range(self.rows):
            row_list = []
            for c in range(self.cols):
                row_list.append(None) 
            self.buttons.append(row_list)
        
        self.create_grid()
        self.place_mines()
        self.count_neighbors()

    def create_grid(self):
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=20, pady=20)

        for r in range(self.rows):
            for c in range(self.cols):
                bttn = tk.Button(self.game_frame, width=3)
                bttn.bind("<Button-1>", lambda e, r=r, c=c: self.handle_reveal(r, c))
                bttn.bind("<Button-3>", lambda e, r=r, c=c: self.handle_flag(r, c))
                bttn.grid(row=r, column=c)
                self.buttons[r][c] = bttn

    def place_mines(self):
        all_positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                all_positions.append([r,c])
        self.mine_locations = random.sample(all_positions, self.mines_count)
        for r, c in self.mine_locations:
            self.logic_board[r][c] = "M"

    def count_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.logic_board[r][c] == "M":
                    continue
                
                mine_sum = 0
                for surroundingrow in [-1, 0, 1]:
                    for surroundingcolumn in [-1, 0, 1]:
                        nr, nc = r + surroundingrow, c + surroundingcolumn
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.logic_board[nr][nc] == "M":
                                mine_sum += 1
                self.logic_board[r][c] = mine_sum

    def handle_reveal(self, r, c):
        if self.buttons[r][c]['text'] == "F":
            returnc

        if self.logic_board[r][c] == "M":
            self.show_all_mines()
            self.end_game("You hit a mine! You Lost.")
        else:
            self.reveal_area(r, c)
            if self.revealed_count == 119:
                self.end_game("You revealed all safe cells! You Win!")

    def reveal_area(self, r, c):
        bttn = self.buttons[r][c]
        if bttn['state'] == 'disabled':
            return

        value = self.logic_board[r][c]
        bttn.config(state='disabled', relief='sunken', bg="#d1d1d1")
        self.revealed_count += 1

        if value > 0:
            bttn.config(text=value)
        else:
            for surroundingrow in [-1, 0, 1]:
                for surroundingcolumn in [-1, 0, 1]:
                    nr, nc = r + surroundingrow, c + surroundingcolumn
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal_area(nr, nc)

    def handle_flag(self, r, c):
        bttn = self.buttons[r][c]
        if bttn['state'] == 'disabled':
            return
        
        if bttn['text'] == "F":
            bttn.config(text="")
        else:
            bttn.config(text="F", fg="red")

    def show_all_mines(self):
        for r, c in self.mine_locations:
            self.buttons[r][c].config(text="M", bg="red")

    def end_game(self, message):
        self.game_over = True
        if messagebox.askyesno("Game Over", f"{message}\n\nDo you want to play again?"):
            self.restart()
        else:
            self.quit_app()

    def restart(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.start_game()

root = tk.Tk()
MinesweeperGame(root)
root.mainloop()