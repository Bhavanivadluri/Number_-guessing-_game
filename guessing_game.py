import tkinter as tk
from tkinter import messagebox
import random
import winsound  # Built-in Windows sound module

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("420x400")
        self.root.resizable(False, False)

        self.difficulty_settings = {
            "Easy": (1, 50, 10),
            "Medium": (1, 100, 7),
            "Hard": (1, 200, 5)
        }

        self.create_widgets()
        self.set_difficulty("Easy")

    def create_widgets(self):
        tk.Label(self.root, text="Select Difficulty:", font=("Arial", 12)).pack(pady=5)
        self.difficulty_var = tk.StringVar(value="Easy")
        for level in self.difficulty_settings:
            tk.Radiobutton(self.root, text=level, variable=self.difficulty_var,
                           value=level, command=self.change_difficulty).pack()

        self.label_intro = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_intro.pack(pady=10)

        self.entry_guess = tk.Entry(self.root, font=("Arial", 14))
        self.entry_guess.pack(pady=5)

        self.button_check = tk.Button(self.root, text="Check", command=self.check_guess, font=("Arial", 12))
        self.button_check.pack(pady=5)

        self.label_result = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_result.pack(pady=10)

        self.label_attempts = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_attempts.pack(pady=5)

        self.button_restart = tk.Button(self.root, text="Restart Game", command=self.restart_game, font=("Arial", 12))
        self.button_restart.pack(pady=5)

    def set_difficulty(self, level):
        self.level = level
        self.low, self.high, self.max_attempts = self.difficulty_settings[level]
        self.secret_number = random.randint(self.low, self.high)
        self.attempts_left = self.max_attempts

        self.label_intro.config(text=f"Guess a number between {self.low} and {self.high}")
        self.label_attempts.config(text=f"Attempts Left: {self.attempts_left}")
        self.label_result.config(text="")
        self.entry_guess.delete(0, tk.END)
        self.button_check.config(state=tk.NORMAL)

    def change_difficulty(self):
        selected = self.difficulty_var.get()
        self.set_difficulty(selected)

    def check_guess(self):
        try:
            guess = int(self.entry_guess.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            return

        if guess < self.low or guess > self.high:
            messagebox.showwarning("Out of Range", f"Guess must be between {self.low} and {self.high}")
            return

        self.attempts_left -= 1
        self.label_attempts.config(text=f"Attempts Left: {self.attempts_left}")

        if guess == self.secret_number:
            self.label_result.config(text="🎉 Correct! You win!")
            winsound.MessageBeep(winsound.MB_OK)  # Play simple beep sound
            self.button_check.config(state=tk.DISABLED)
        elif guess < self.secret_number:
            self.label_result.config(text="Too low! Try again.")
            winsound.MessageBeep(winsound.MB_ICONHAND)  # Different beep for wrong guess
        else:
            self.label_result.config(text="Too high! Try again.")
            winsound.MessageBeep(winsound.MB_ICONHAND)

        if self.attempts_left == 0 and guess != self.secret_number:
            self.label_result.config(text=f"❌ Game Over! The number was {self.secret_number}")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            self.button_check.config(state=tk.DISABLED)

    def restart_game(self):
        self.set_difficulty(self.difficulty_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
