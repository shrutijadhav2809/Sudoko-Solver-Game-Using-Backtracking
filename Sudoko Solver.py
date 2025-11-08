import tkinter as tk
from tkinter import messagebox
import time

# ---------------- Sudoku Board ----------------
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Copy of original puzzle (to lock fixed cells)
original_board = [row[:] for row in board]

# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("Sudoku - Backtracking Demo")

PASTEL_BG = "#d8e9f0"
PASTEL_GREEN = "#9be8c7"
PASTEL_RED = "#f5a3a3"

root.configure(bg=PASTEL_BG)
root.geometry("720x720")
root.minsize(680, 680)
root.eval('tk::PlaceWindow . center')

controls = tk.Frame(root, bg=PASTEL_BG)
controls.pack(pady=6)

start_btn = tk.Button(controls, text="Start Playing", width=14,
                      bg="#2563eb", fg="white", font=("Helvetica", 11, "bold"))
enter_btn = tk.Button(controls, text="Enter Value", width=12,
                      bg="#22c55e", fg="white", font=("Helvetica", 11, "bold"))
enter_btn.config(state="disabled")

start_btn.grid(row=0, column=0, padx=6)
enter_btn.grid(row=0, column=1, padx=6)

cell_size = 60
canvas = tk.Canvas(root, width=540, height=540, bg="white",
                   highlightthickness=2, highlightbackground="#333")
canvas.pack(pady=12)

# ---------------- Drawing ----------------
cell_colors = [[None for _ in range(9)] for _ in range(9)]

def draw_grid():
    canvas.delete("grid")
    for i in range(10):
        w = 3 if i % 3 == 0 else 1
        canvas.create_line(0, i * cell_size, 540, i * cell_size, width=w, tags="grid")
        canvas.create_line(i * cell_size, 0, i * cell_size, 540, width=w, tags="grid")

def draw_dots():
    canvas.delete("numbers")
    for r in range(9):
        for c in range(9):
            canvas.create_text(c * cell_size + 30, r * cell_size + 30,
                               text="•", fill="#bbb", font=("Helvetica", 20, "bold"),
                               tags="numbers")

def draw_numbers():
    canvas.delete("numbers", "cells")
    for r in range(9):
        for c in range(9):
            color = cell_colors[r][c]
            if color:
                x1, y1 = c * cell_size, r * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="cells")
            val = board[r][c]
            if val:
                canvas.create_text(c * cell_size + 30, r * cell_size + 30,
                                   text=str(val), fill="black",
                                   font=("Helvetica", 18, "bold"), tags="numbers")
            else:
                canvas.create_text(c * cell_size + 30, r * cell_size + 30,
                                   text=".", fill="#999",
                                   font=("Helvetica", 14), tags="numbers")

def is_valid(r, c, num):
    if num in board[r]: return False
    for i in range(9):
        if board[i][c] == num: return False
    sr, sc = (r // 3) * 3, (c // 3) * 3
    for i in range(sr, sr + 3):
        for j in range(sc, sc + 3):
            if board[i][j] == num: return False
    return True

# ---------------- Interactions ----------------
def start_playing():
    start_btn.config(state="disabled")
    enter_btn.config(state="normal")
    draw_numbers()

def bring_to_front(win):
    win.attributes("-topmost", True)
    win.lift()
    win.focus_force()

def enter_value():
    pop = tk.Toplevel(root)
    pop.title("Enter Value")
    pop.configure(bg=PASTEL_BG)
    pop.geometry("280x220")
    pop.resizable(False, False)
    bring_to_front(pop)

    def labeled_entry(parent, text):
        lab = tk.Label(parent, text=text, bg=PASTEL_BG, font=("Helvetica", 11))
        ent = tk.Entry(parent, justify="center", font=("Helvetica", 12), width=10)
        lab.pack(pady=(8, 2))
        ent.pack()
        return ent

    row_e = labeled_entry(pop, "Row (1–9)")
    col_e = labeled_entry(pop, "Column (1–9)")
    num_e = labeled_entry(pop, "Number (1–9)")

    def submit():
        try:
            r = int(row_e.get()) - 1
            c = int(col_e.get()) - 1
            n = int(num_e.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter integers 1–9.")
            bring_to_front(pop)
            return

        pop.destroy()

        if not (0 <= r < 9 and 0 <= c < 9 and 1 <= n <= 9):
            messagebox.showwarning("Invalid", "Values must be between 1–9.")
            return

        # ❌ Prevent changes to original fixed Sudoku cells
        if original_board[r][c] != 0:
            messagebox.showinfo("Locked Cell", f"Cell ({r+1},{c+1}) is part of the original puzzle and cannot be changed.")
            return

        # ✅ Allow user to overwrite their own previously entered value
        board[r][c] = 0  # Clear before checking new value

        if is_valid(r, c, n):
            board[r][c] = n
            cell_colors[r][c] = PASTEL_GREEN
            draw_numbers()
            messagebox.showinfo("Placed", f"✅ {n} placed successfully at ({r+1},{c+1}).")
        else:
            board[r][c] = n  # Still show attempted number
            cell_colors[r][c] = PASTEL_RED
            draw_numbers()
            messagebox.showerror("Backtrack", f"❌ Invalid at ({r+1},{c+1}) — Backtrack.")

    tk.Button(pop, text="Submit", width=16, height=2, bg="#2563eb", fg="white",
              font=("Helvetica", 12, "bold"), command=submit).pack(pady=16)
    bring_to_front(pop)

# Bind buttons
start_btn.config(command=start_playing)
enter_btn.config(command=enter_value)

# Initial draw: grid + dots
draw_grid()
draw_dots()

root.mainloop()
