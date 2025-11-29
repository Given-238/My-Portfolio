"""
GUI Quiz Game (Tkinter) with:
- questions loaded from questions.txt
- difficulty select (EASY / MEDIUM / HARD)
- 10s timer per question with progress bar
- animations (background flash + button color)
- sound effects via pygame
- scoreboard stored in scoreboard.json
"""

import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import random
import threading
import time
import json
import os
from datetime import datetime

# sounds might be skipped
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SCOREBOARD_FILE = os.path.join(BASE_DIR, "scoreboard.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.txt")

# -------------------------
# Sound helper
# -------------------------
def init_sound():
    if not PYGAME_AVAILABLE:
        return False
    pygame.mixer.init()
    return True

def play_sound(filename):
    if not PYGAME_AVAILABLE:
        return
    path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(path):
        try:
            sound = pygame.mixer.Sound(path)
            sound.play()
        except Exception:
            pass

# -------------------------
# Questions loader
# -------------------------
def load_questions(filename=QUESTIONS_FILE):
    """
    Load questions grouped by difficulty from a text file.
    Format per block:
      DIFFICULTY
      Q: question text
      A: correct answer
      OPTIONS: option1, option2, option3, option4
    Blocks separated by a blank line.
    """
    banks = {"EASY": [], "MEDIUM": [], "HARD": []}
    if not os.path.exists(filename):
        return banks

    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    if raw == "":
        return banks

    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 4:
            continue
        diff = lines[0].strip().upper()
        q_line = lines[1].strip()
        a_line = lines[2].strip()
        options_line = lines[3].strip()

        if not q_line.startswith("Q:") or not a_line.startswith("A:") or not options_line.startswith("OPTIONS:"):
            continue

        question = q_line.replace("Q:", "").strip()
        answer = a_line.replace("A:", "").strip()
        options = [opt.strip() for opt in options_line.replace("OPTIONS:", "").split(",")]

        if diff in banks:
            banks[diff].append({"question": question, "answer": answer, "options": options})

    return banks

# -------------------------
# Scoreboard helpers
# -------------------------
def load_scoreboard():
    if not os.path.exists(SCOREBOARD_FILE):
        return []
    try:
        with open(SCOREBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_scoreboard(scoreboard):
    try:
        with open(SCOREBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(scoreboard, f, indent=4)
    except Exception:
        pass

def add_score(name, score, total):
    board = load_scoreboard()
    entry = {"name": name, "score": score, "total": total, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    board.append(entry)
    # keep only latest 100 entries to avoid huge file
    board = board[-100:]
    save_scoreboard(board)

# -------------------------
# GUI App
# -------------------------
class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Game — GUI")
        master.geometry("700x480")
        master.resizable(False, False)
        self.master.configure(bg="#f6f8fa")

        # load resources
        self.question_bank = load_questions()
        self.difficulty = None
        self.questions = []
        self.index = 0
        self.score = 0
        self.time_left = 10
        self.timer_running = False

        # top frame
        self.header = tk.Frame(master, bg="#0d47a1", height=80)
        self.header.pack(fill="x")
        title = tk.Label(self.header, text="Quiz Game", bg="#0d47a1", fg="white", font=("Segoe UI", 20, "bold"))
        title.pack(pady=18)

        # central frame
        self.frame = tk.Frame(master, bg="#f6f8fa")
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_difficulty_screen()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    # difficulty selection screen
    def create_difficulty_screen(self):
        self.clear_frame()
        lbl = tk.Label(self.frame, text="Select Difficulty", bg="#f6f8fa", font=("Segoe UI", 16))
        lbl.pack(pady=20)

        btn_easy = tk.Button(self.frame, text="Easy", width=20, height=2, command=lambda: self.start_quiz("EASY"))
        btn_medium = tk.Button(self.frame, text="Medium", width=20, height=2, command=lambda: self.start_quiz("MEDIUM"))
        btn_hard = tk.Button(self.frame, text="Hard", width=20, height=2, command=lambda: self.start_quiz("HARD"))

        btn_easy.pack(pady=8)
        btn_medium.pack(pady=8)
        btn_hard.pack(pady=8)

        bottom_frame = tk.Frame(self.frame, bg="#f6f8fa")
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        view_scores_btn = tk.Button(bottom_frame, text="View Scoreboard", command=self.show_scoreboard)
        view_scores_btn.pack(side="right", padx=10)

    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.questions = list(self.question_bank.get(difficulty, []))[:]
        if not self.questions:
            messagebox.showinfo("No questions", f"No {difficulty} questions found. Please add questions to questions.txt")
            return
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_frame()
        if self.index >= len(self.questions):
            self.show_final_screen()
            return

        q = self.questions[self.index]
        question_text = q["question"]
        options = q["options"]

        # timer / progress
        self.time_left = 10
        self.timer_running = True

        tl_frame = tk.Frame(self.frame, bg="#f6f8fa")
        tl_frame.pack(fill="x", pady=4)
        self.timer_label = tk.Label(tl_frame, text=f"Time left: {self.time_left}s", bg="#f6f8fa", font=("Segoe UI", 12))
        self.timer_label.pack(side="left", padx=6)
        self.progress = ttk.Progressbar(tl_frame, orient="horizontal", length=400, mode="determinate", maximum=10)
        self.progress.pack(side="left", padx=20)
        self.progress['value'] = 10

        # question
        q_label = tk.Label(self.frame, text=question_text, bg="#f6f8fa", wraplength=620, font=("Segoe UI", 14))
        q_label.pack(pady=18)

        # option buttons
        self.option_buttons = []
        for opt in options:
            btn = tk.Button(self.frame, text=opt, wraplength=500, width=50, anchor="w",
                            command=lambda choice=opt: self.handle_answer(choice))
            btn.pack(pady=6)
            self.option_buttons.append(btn)

        # small hint label
        hint = tk.Label(self.frame, text=f"Question {self.index+1} of {len(self.questions)}", bg="#f6f8fa", font=("Segoe UI", 10, "italic"))
        hint.pack(pady=10)

        # start timer loop
        self.master.after(1000, self.timer_tick)

    def timer_tick(self):
        if not self.timer_running:
            return
        self.time_left -= 1
        if self.time_left < 0:
            # times up
            self.timer_running = False
            self.animate_feedback(correct=False, timed_out=True)
            self.master.after(700, lambda: self.next_question())
            return
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.progress['value'] = self.time_left
        self.master.after(1000, self.timer_tick)

    def handle_answer(self, chosen):
        if not self.timer_running:
            return  # ignore double clicks or late input
        correct_answer = self.questions[self.index]['answer']
        self.timer_running = False
        if chosen == correct_answer:
            self.score += 1
            self.animate_feedback(correct=True)
        else:
            self.animate_feedback(correct=False)
        # delay to show feedback
        self.master.after(700, lambda: self.next_question())

    def animate_feedback(self, correct=True, timed_out=False):
        # play sound
        if correct and not timed_out:
            play_sound("correct.wav")
        else:
            play_sound("wrong.wav")

        # flash background color
        original = self.master.cget("bg")
        color = "#c8e6c9" if correct and not timed_out else "#ffcccb"
        self.master.configure(bg=color)
        self.frame.configure(bg=color)
        self.header.configure(bg=color)
        self.master.after(500, lambda: self.reset_bg(original))

    def reset_bg(self, color):
        self.master.configure(bg=color)
        self.frame.configure(bg="#f6f8fa")
        self.header.configure(bg="#0d47a1")

    def next_question(self):
        self.index += 1
        self.show_question()

    def show_final_screen(self):
        self.clear_frame()
        lbl = tk.Label(self.frame, text="Quiz Complete!", bg="#f6f8fa", font=("Segoe UI", 20, "bold"))
        lbl.pack(pady=10)
        score_lbl = tk.Label(self.frame, text=f"Your Score: {self.score} / {len(self.questions)}", bg="#f6f8fa", font=("Segoe UI", 16))
        score_lbl.pack(pady=10)

        # ask player name and save
        name = simpledialog.askstring("Name", "Enter your name to save your score (or Cancel to skip):", parent=self.master)
        if name:
            add_score(name, self.score, len(self.questions))
            save_text = tk.Label(self.frame, text="Score saved to scoreboard.", bg="#f6f8fa")
            save_text.pack(pady=6)
        else:
            skip_text = tk.Label(self.frame, text="Score not saved.", bg="#f6f8fa")
            skip_text.pack(pady=6)

        btn_frame = tk.Frame(self.frame, bg="#f6f8fa")
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Play Again", command=self.create_difficulty_screen).pack(side="left", padx=8)
        tk.Button(btn_frame, text="View Scoreboard", command=self.show_scoreboard).pack(side="left", padx=8)

    def show_scoreboard(self):
        board = load_scoreboard()
        # create a popup window to display scoreboard
        win = tk.Toplevel(self.master)
        win.title("Scoreboard")
        win.geometry("500x400")
        win.configure(bg="#f6f8fa")

        lbl = tk.Label(win, text="Scoreboard (most recent last)", bg="#f6f8fa", font=("Segoe UI", 14, "bold"))
        lbl.pack(pady=8)

        canvas = tk.Canvas(win, bg="#f6f8fa")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(win, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        frame = tk.Frame(canvas, bg="#f6f8fa")
        canvas.create_window((0,0), window=frame, anchor='nw')

        for entry in reversed(board):
            text = f"{entry['date']} — {entry['name']} — {entry['score']}/{entry['total']}"
            tk.Label(frame, text=text, bg="#f6f8fa", anchor="w").pack(fill="x", padx=10, pady=4)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

# -------------------------
# Program start
# -------------------------
def main():
    if PYGAME_AVAILABLE:
        init_sound()
    else:
        print("pygame not installed — sounds disabled. To enable sounds: pip install pygame")

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()