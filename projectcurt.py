import tkinter as tk
import random
from tkinter import messagebox
import sys

class MinesweeperGame:
    """A class to represent the Minesweeper game logic and GUI.
    
    Attributes:
        master (tk.Tk): The root window of the application.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        mines_count (int): Total number of mines to be placed."""
    def __init__(self, master):
        """Initializes the game window and starts the first game instance."""
        self.master = master
        self.master.title("Minesweeper")
        self.start_game()

    def quit_app(self):
        """Closes the game."""
        sys.exit()

    def start_game(self):
        """Sets initial game state variables and creates the logic board."""
        self.rows = 12
        self.cols = 12
        self.mines_count = 25
        self.revealed_count = 0
        self.game_over = False
        self.firstclick = True
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

    def create_grid(self):
        """Generates the Tkinter button grid and binds mouse events."""
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=20, pady=20)

        for r in range(self.rows):
            for c in range(self.cols):
                bttn = tk.Button(self.game_frame, width=3)
                bttn.bind("<Button-1>", lambda e, r=r, c=c: self.handle_reveal(r, c))
                bttn.bind("<Button-3>", lambda e, r=r, c=c: self.handle_flag(r, c))
                bttn.grid(row=r, column=c)
                self.buttons[r][c] = bttn

    def place_mines(self, firstr, firstc):
        """Randomly places mines on the logic board after the first click"""
        all_positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if r == firstr and c == firstc:
                    continue
                all_positions.append([r,c])
        self.mine_locations = random.sample(all_positions, self.mines_count)
        for r, c in self.mine_locations:
            self.logic_board[r][c] = "M"

    def count_neighbors(self):
        """Calculates the number of adjacent mines for every safe cell."""
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
        """Handles the logic when a cell is clicked."""
        if self.buttons[r][c]["state"] == "disabled":
            value = self.logic_board[r][c]
            if value != "M" and value > 0:
                self.reveal_non_flags(r, c, value)
            return
        
        if self.buttons[r][c]['text'] == "F":
            return
        
        if self.firstclick:
            self.firstclick = False
            self.place_mines(r, c)
            self.count_neighbors()

        if self.logic_board[r][c] == "M":
            self.show_all_mines()
            self.end_game("You hit a mine! You Lost.")
        else:
            self.reveal_area(r, c)
            if self.revealed_count == (self.rows * self.cols) - self.mines_count:
                self.end_game("You revealed all safe cells! You Win!")

    def reveal_non_flags(self, r, c, value):
        """Reveals neighbors if the number of flags matches the cell value."""
        flag_count = 0
        for surroundingrow in [-1, 0, 1]:
            for surroundingcol in [-1, 0, 1]:
                nr, nc = r + surroundingrow, c + surroundingcol
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.buttons[nr][nc]["text"] == "F":
                        flag_count += 1
        if flag_count == value:
            for surroundingrow in [-1, 0, 1]:
                for surroundingcol in [-1, 0, 1]:
                    nr, nc = r + surroundingrow, c + surroundingcol
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.buttons[nr][nc]["text"] != "F" and self.buttons[nr][nc]["state"] != "disabled":
                            if self.logic_board[nr][nc] == "M":
                                self.show_all_mines()
                                self.end_game("Wrong placement of flags! you hit a mine.")
                                return
                            else:
                                self.reveal_area(nr, nc)

    def reveal_area(self, r, c):
        """Recursively reveals empty areas (0-neighbor cells)."""
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
        """Toggles a flag 'F' on right-click to mark potential mines."""
        bttn = self.buttons[r][c]
        if bttn['state'] == 'disabled':
            return
        
        if bttn['text'] == "F":
            bttn.config(text="")
        else:
            bttn.config(text="F", fg="red")

    def show_all_mines(self):
        """Reveals all mine locations when the game is lost."""
        for r, c in self.mine_locations:
            self.buttons[r][c].config(text="M", bg="red")

    def end_game(self, message):
        """Displays the win/loss message and handles restart logic."""
        self.game_over = True
        if messagebox.askyesno("Game Over", f"{message}\n\nDo you want to play again?"):
            self.restart()
        else:
            self.quit_app()

    def restart(self):
        """Clears the board and starts a new game."""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.start_game()

root = tk.Tk()
MinesweeperGame(root)
root.mainloop()
