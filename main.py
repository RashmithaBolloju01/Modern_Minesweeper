import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage, ttk
import random
import sys
import os
import csv


from sound_manager import SoundManager


sound_manager = SoundManager(enabled=True)

# Game constants
WIDTH = 500
HEIGHT = 600
app_path = "."

# Modern dark theme colors
COLORS = {
    "bg_dark": "#1e1e2f",
    "panel": "#2c2f4a",
    "accent": "#00e5ff",
    "accent_alt": "#ffcc00",
    "text_light": "#ffffff",
    "text_muted": "#b0b0b0",
    "cell_light": "#e0e0e0",
    "cell_hover": "#f0f0f0",
    "easy": "#4CAF50",
    "medium": "#FF9800",
    "hard": "#F44336",
}

# Difficulty presets
DIFFICULTY_PRESETS = {
    "Easy": {"grid_size": 6, "mines": 10},
    "Medium": {"grid_size": 8, "mines": 8},
    "Hard": {"grid_size": 10, "mines": 30},
}

# Game variables (will be set based on difficulty)
GRID_SIZE = 8
MINES_COUNT = 8
CELL_COUNT = GRID_SIZE**2
gameRunning = False
time = 0

# Feedback system variable
feedback_label = None
feedback_timer = None

# UI Elements
window = None
start_menu_frame = None
game_frame = None
centre_frame = None
timer_label = None
mines_left_label = None


if not os.path.isfile(f"{app_path}/leaderboard.csv"):
    with open(f"{app_path}/leaderboard.csv", "w", newline="") as file:
        pass


def height_prct(percentage):
    return (HEIGHT / 100) * percentage


def width_prct(percentage):
    return (WIDTH / 100) * percentage


def show_feedback(text):
    """
    Display animated feedback text at the center of the window.
    Automatically disappears after 2 seconds.
    Only one feedback label exists at a time.
    
    Args:
        text: The feedback message to display
    """
    global feedback_label, feedback_timer
    
    # Destroy previous feedback label if it exists
    if feedback_label is not None:
        if feedback_timer is not None:
            window.after_cancel(feedback_timer)
        feedback_label.destroy()
    
    # Create new feedback label
    feedback_label = tk.Label(
        window,
        text=text,
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#FFD700",
        padx=20,
        pady=10,
        relief=tk.RAISED,
        borderwidth=2
    )
    feedback_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Schedule disappearance after 2 seconds
    feedback_timer = window.after(2000, lambda: destroy_feedback())


def destroy_feedback():
    """Destroy the feedback label safely."""
    global feedback_label, feedback_timer
    
    if feedback_label is not None:
        try:
            feedback_label.destroy()
            feedback_label = None
            feedback_timer = None
        except tk.TclError:
            # Label already destroyed
            feedback_label = None
            feedback_timer = None


class Cell:
    cells_left = CELL_COUNT
    mines_left = MINES_COUNT
    all = []

    def __init__(self, x, y):
        self.is_mine = False
        self.is_opened = False
        self.is_marked = False
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn(self, location):
        btn = tk.Button(location, width=4, height=2)
        btn.bind("<Button-1>", self.left_click)
        btn.bind("<Button-3>", self.right_click)
        self.cell_btn_obj = btn

    def left_click(self, event):
        global gameRunning, time
        if self.is_mine:
            self.reveal_mine()
        else:
            self.reveal_cell()
            if Cell.cells_left == MINES_COUNT:
                gameRunning = False
                sound_manager.play_win()
                show_feedback("Victory!")
                messagebox.showinfo("Game Over", "Congratulations! You won the game.")

                write_lb()
                reset_game()

    def right_click(self, event):
        if not self.is_marked:
            self.cell_btn_obj.configure(bg="orange")
            self.is_marked = True
            Cell.mines_left -= 1
            mines_left_label.configure(text=Cell.mines_left)
            self.cell_btn_obj.unbind("<Button-1>")
            sound_manager.play_flag()
        else:
            self.cell_btn_obj.configure(bg="SystemButtonFace")
            self.is_marked = False
            Cell.mines_left += 1
            mines_left_label.configure(text=Cell.mines_left)
            self.cell_btn_obj.bind("<Button-1>", self.left_click)
            sound_manager.play_flag()

    def reveal_mine(self):
        global gameRunning
        gameRunning = False
        sound_manager.play_boom()
        show_feedback("BOOM!")
        self.cell_btn_obj.configure(bg="red")
        messagebox.showinfo("Game Over", "You Clicked on a Mine!")
        reset_game()

    def reveal_cell(self):
        if not self.is_opened:
            sound_manager.play_click()
            self.cell_btn_obj.configure(
                text=self.surrounded_mines if self.surrounded_mines != 0 else "",
                bg="lightgrey",
            )
            self.is_opened = True
            Cell.cells_left -= 1
            
            # Show feedback for safe cell reveal
            show_feedback("Nice Move!")

            if self.is_marked:
                Cell.mines_left += 1
                mines_left_label.configure(text=Cell.mines_left)

            self.cell_btn_obj.unbind("<Button-1>")
            self.cell_btn_obj.unbind("<Button-3>")

            if self.surrounded_mines == 0:
                # Show "Great!" when multiple cells are revealed
                show_feedback("Great!")
                for cell_obj in self.surrounded_cells:
                    cell_obj.reveal_cell()

    def get_cell(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        surr_cells = [
            self.get_cell(self.x - 1, self.y - 1),
            self.get_cell(self.x, self.y - 1),
            self.get_cell(self.x + 1, self.y - 1),
            self.get_cell(self.x - 1, self.y),
            self.get_cell(self.x + 1, self.y),
            self.get_cell(self.x - 1, self.y + 1),
            self.get_cell(self.x, self.y + 1),
            self.get_cell(self.x + 1, self.y + 1),
        ]
        surr_cells = [cell for cell in surr_cells if cell is not None]
        return surr_cells

    @property
    def surrounded_mines(self):
        mines_nearby = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                mines_nearby += 1
        return mines_nearby

    @staticmethod
    def create_mines():
        mines = random.sample(Cell.all, MINES_COUNT)
        for mine in mines:
            mine.is_mine = True

    def __repr__(self):
        return f"({self.x},{self.y})"


def reset_game():
    """Clear the board and return to the start menu."""
    global gameRunning, time, game_frame, start_menu_frame
    
    gameRunning = False
    time = 0
    
    # Clear Cell class data
    Cell.all = []
    Cell.cells_left = CELL_COUNT
    Cell.mines_left = MINES_COUNT
    
    # Hide game frame and show start menu
    game_frame.pack_forget()
    start_menu_frame.pack(expand=True, fill=tk.BOTH)
    
    # Clean up feedback
    destroy_feedback()


def update_timer():
    global gameRunning, time
    if gameRunning:
        time += 1
        timer_label["text"] = f"{time}s"
        window.after(1000, update_timer)
    else:
        window.after(1000, update_timer)


def write_lb():
    while True:
        pname = simpledialog.askstring(title="Minesweeper", prompt="What's your Name?:")
        if pname != "":
            break
        else:
            messagebox.showerror("Invalid", "Please enter name")

    if pname != None:
        with open(f"{app_path}/leaderboard.csv", "a", newline="") as file:
            cw = csv.writer(file)
            cw.writerow((pname, f"{time}s"))
    clear_lb(f"{app_path}/leaderboard.csv", 10)


def clear_lb(file, limit):
    with open(file) as f:
        cr = csv.reader(f)
        res = list(cr)
    if len(res) > limit:
        res.pop(0)
        with open(file, "w", newline="") as f:
            cw = csv.writer(f)
            cw.writerows(res)


def show_lb():
    global gameRunning
    gameRunning = False
    window.withdraw()
    lbwin = tk.Toplevel(window)
    lbwin.title("Leaderboard")
    lbwin.geometry("360x220")
    with open(f"{app_path}/leaderboard.csv") as file:
        cr = csv.reader(file)
        lbdata = list(cr)
    table = ttk.Treeview(lbwin, columns=("c1", "c2"), show="headings")
    table.column("#1", anchor=tk.CENTER)
    table.heading("#1", text="Name")
    table.column("#2", anchor=tk.CENTER)
    table.heading("#2", text="Highscore")
    table.pack()
    for row in lbdata:
        table.insert("", tk.END, values=row)

    window.wait_window(lbwin)
    window.deiconify()
    gameRunning = True


def start_game(difficulty):
    """
    Initialize and start the game with the selected difficulty.
    
    Args:
        difficulty: String key from DIFFICULTY_PRESETS ("Easy", "Medium", "Hard")
    """
    global GRID_SIZE, MINES_COUNT, CELL_COUNT, gameRunning, time
    global start_menu_frame, game_frame, centre_frame
    global timer_label, mines_left_label
    
    # Set difficulty parameters
    preset = DIFFICULTY_PRESETS[difficulty]
    GRID_SIZE = preset["grid_size"]
    MINES_COUNT = preset["mines"]
    CELL_COUNT = GRID_SIZE**2
    
    # Reset Cell class data
    Cell.all = []
    Cell.cells_left = CELL_COUNT
    Cell.mines_left = MINES_COUNT
    
    # Hide start menu and show game frame
    start_menu_frame.pack_forget()
    game_frame.pack(expand=True, fill=tk.BOTH)
    
    # Clear previous game board if it exists
    for widget in centre_frame.winfo_children():
        widget.destroy()
    
    # Create game buttons
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            c = Cell(x, y)
            c.create_btn(centre_frame)
            c.cell_btn_obj.grid(column=x, row=y)
    
    # Create mines
    Cell.create_mines()
    
    # Reset game state
    gameRunning = True
    time = 0
    timer_label["text"] = "0s"
    mines_left_label.configure(text=Cell.mines_left)
    
    # Start timer
    window.after(1000, update_timer)


def create_start_menu():
    """Create the start menu screen with difficulty selection."""
    global start_menu_frame
    
    start_menu_frame = tk.Frame(window, bg=COLORS["bg_dark"])
    start_menu_frame.pack(expand=True, fill=tk.BOTH)
    
    # Title
    title_label = tk.Label(
        start_menu_frame,
        text="MINESWEEPER",
        bg=COLORS["bg_dark"],
        fg="#00e5ff",
        font=("Arial", 40, "bold")
    )
    title_label.pack(pady=40)
    
    # Subtitle
    subtitle_label = tk.Label(
        start_menu_frame,
        text="Select Difficulty",
        bg=COLORS["bg_dark"],
        fg="#cccccc",
        font=("Arial", 18)
    )
    subtitle_label.pack(pady=10)
    
    # Button frame
    button_frame = tk.Frame(start_menu_frame, bg=COLORS["bg_dark"])
    button_frame.pack(pady=30)
    
    # Easy button
    easy_btn = tk.Button(
    button_frame,
    text="Easy\n(6x6, 10 mines)",
    width=20,
    height=3,
    font=("Arial", 14, "bold"),
    bg="#00c853",          # bright green
    fg="black",            # FIX: text visible
    activebackground="#69f0ae",
    bd=2,
    relief="raised",
    highlightthickness=1,
    command=lambda: start_game("Easy")
)
    easy_btn.pack(pady=10)
    
    # Medium button
    medium_btn = tk.Button(
    button_frame,
    text="Medium\n(8x8, 8 mines)",
    width=20,
    height=3,
    font=("Arial", 14, "bold"),
    bg="#ffab00",          # amber
    fg="black",
    activebackground="#ffd740",
    bd=2,
    relief="raised",
    highlightthickness=1,
    command=lambda: start_game("Medium")
)
    medium_btn.pack(pady=10)
    
    # Hard button
    hard_btn = tk.Button(
    button_frame,
    text="Hard\n(10x10, 30 mines)",
    width=20,
    height=3,
    font=("Arial", 14, "bold"),
    bg="#ff1744",
    fg="white",
    activebackground="#ff5252",
    activeforeground="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    borderwidth=0,
    command=lambda: start_game("Hard")
)

    hard_btn.pack(pady=10)

    hard_btn.configure(highlightbackground="#ff1744")



def create_game_screen():
    """Create the game screen layout."""
    global game_frame, centre_frame, timer_label, mines_left_label
    
    game_frame = tk.Frame(window, bg=COLORS["bg_dark"])
    
    # Top frame with title
    top_frame = tk.Frame(game_frame, bg=COLORS["panel"], width=WIDTH, height=height_prct(10))
    top_frame.pack()
    
    title_label = tk.Label(
        top_frame, text="MINESWEEPER", bg=COLORS["panel"], fg="#00e5ff", font=("Arial", 28)
    )
    title_label.pack(pady=10)
    
    # Info frame with timer and mines count
    info_frame = tk.Frame(game_frame, bg=COLORS["panel"], width=WIDTH, height=height_prct(8))
    info_frame.pack()
    
    timer_label = tk.Label(
        info_frame,
        font=("verdana", 12),
        fg=COLORS["text_light"],
        text="0s",
        width=10,
        bg=COLORS["panel"],
    )
    timer_label.pack(side=tk.LEFT, padx=20)
    
    mines_left_label = tk.Label(
        info_frame,
        font=("verdana", 12),
        fg=COLORS["text_light"],
        bg=COLORS["panel"],
        text=Cell.mines_left,
    )
    mines_left_label.pack(side=tk.LEFT, padx=20)
    
    leaderboard_btn = tk.Button(
        info_frame,
        text="Leaderboard",
        command=show_lb,
    )
    leaderboard_btn.pack(side=tk.RIGHT, padx=20, pady=5)
    
    # Game board frame
    centre_frame = tk.Frame(
        game_frame, bg="black", width=width_prct(75), height=height_prct(75)
    )
    centre_frame.pack(pady=10)


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.title("Minesweeper")

    app_icon = PhotoImage(file=f"{app_path}/appicon.png")
    window.iconphoto(True, app_icon)

    window.configure(bg=COLORS["bg_dark"])
    window.resizable(False, False)

    # Create both screens
    create_start_menu()
    create_game_screen()
    
    # Start with the menu screen visible
    start_menu_frame.pack(expand=True, fill=tk.BOTH)

    window.mainloop()
