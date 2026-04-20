import tkinter as tk
from tkinter import messagebox
import threading

# ---------------- SOLVER (Backtracking) ---------------- #

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, num, pos):
    row, col = pos

    for j in range(9):
        if board[row][j] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False

# ---------------- VALIDATION ---------------- #

def is_board_valid(board):
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                board[i][j] = 0
                if not is_valid(board, num, (i, j)):
                    board[i][j] = num
                    return False
                board[i][j] = num
    return True

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Sudoku Solver - Prodigy Task 04")
root.geometry("500x650")
root.configure(bg="#1e1e2f")

main_frame = tk.Frame(root, bg="#1e1e2f")
main_frame.pack(expand=True)

# ---------------- TIMER ---------------- #

time_left = 180  # 3 minutes

timer_label = tk.Label(main_frame, font=("Arial", 14, "bold"), bg="#1e1e2f", fg="white")
timer_label.pack(pady=10)

def update_timer():
    global time_left
    mins = time_left // 60
    secs = time_left % 60

    timer_label.config(text=f"⏱ Time Left: {mins:02}:{secs:02}")

    if time_left > 0:
        time_left -= 1
        root.after(1000, update_timer)
    else:
        messagebox.showinfo("Time Up", "⏰ Time's up!")

# ---------------- GRID ---------------- #

grid_frame = tk.Frame(main_frame, bg="#1e1e2f")
grid_frame.pack()

entries = []

def validate_input(P):
    return P == "" or (P.isdigit() and 1 <= int(P) <= 9)

vcmd = (root.register(validate_input), "%P")

for i in range(9):
    row = []
    for j in range(9):
        e = tk.Entry(
            grid_frame,
            width=3,
            font=("Arial", 20, "bold"),
            justify="center",
            bg="#2a2a40",
            fg="white",
            insertbackground="white",
            validate="key",
            validatecommand=vcmd
        )

        padx = (4 if j % 3 == 0 else 1)
        pady = (4 if i % 3 == 0 else 1)

        e.grid(row=i, column=j, padx=padx, pady=pady, ipady=5)
        row.append(e)
    entries.append(row)

# ---------------- FUNCTIONS ---------------- #

def get_board():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            row.append(int(val) if val else 0)
        board.append(row)
    return board

def display(board):
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(board[i][j]))

def solve_thread():
    solve_btn.config(state="disabled", text="Solving...")

    board = get_board()

    if not is_board_valid(board):
        messagebox.showerror("Invalid Input", "❌ Sudoku rules violated!")
        solve_btn.config(state="normal", text="Solve")
        return

    if solve(board):
        display(board)
    else:
        messagebox.showerror("Error", "No solution exists")

    solve_btn.config(state="normal", text="Solve")

def solve_sudoku():
    threading.Thread(target=solve_thread).start()

def clear_board():
    global time_left
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
    time_left = 180
    update_timer()

# ---------------- BUTTONS ---------------- #

btn_frame = tk.Frame(main_frame, bg="#1e1e2f")
btn_frame.pack(pady=20)

solve_btn = tk.Button(
    btn_frame,
    text="Solve",
    command=solve_sudoku,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10
)
solve_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    command=clear_board,
    bg="#f44336",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10
)
clear_btn.grid(row=0, column=1, padx=10)

# Start timer
update_timer()

root.mainloop()