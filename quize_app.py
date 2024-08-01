import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import time

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.load_questions('questions.json')
        self.question_index = 0
        self.score = 0
        self.time_per_question = 15  # 15 seconds for each question

        self.setup_gui()

    def load_questions(self, filename):
        with open(filename, 'r') as file:
            self.questions = json.load(file)
        random.shuffle(self.questions)

    def setup_gui(self):
        self.start_screen()

    def start_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to the Quiz Application", font=('Arial', 20)).pack(pady=20)
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=('Arial', 14)).pack(pady=20)

    def start_quiz(self):
        self.clear_screen()
        self.setup_quiz_interface()
        self.display_question()

    def setup_quiz_interface(self):
        self.progress_label = tk.Label(self.root, text="", font=('Arial', 14))
        self.progress_label.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", wraplength=400, font=('Arial', 16))
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.root, text="", variable=self.var, value="", font=('Arial', 12))
            btn.pack(anchor='w')
            self.option_buttons.append(btn)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_answer, font=('Arial', 12))
        self.submit_button.pack(pady=20)

        self.next_button = tk.Button(self.root, text="Next Question", command=self.next_question, state=tk.DISABLED, font=('Arial', 12))
        self.next_button.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="", font=('Arial', 14))
        self.timer_label.pack(pady=10)

    def display_question(self):
        self.question_start_time = time.time()
        self.update_timer()

        question_data = self.questions[self.question_index]
        self.progress_label.config(text=f"Question {self.question_index + 1} of {len(self.questions)}")
        self.question_label.config(text=question_data['question'])

        self.var.set(None)

        for i, option in enumerate(question_data['options']):
            self.option_buttons[i].config(text=option, value=option)

        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def update_timer(self):
        elapsed_time = time.time() - self.question_start_time
        remaining_time = max(0, self.time_per_question - int(elapsed_time))
        self.timer_label.config(text=f"Time Remaining: {remaining_time} seconds")

        if remaining_time > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.submit_answer(auto_submit=True)

    def submit_answer(self, auto_submit=False):
        if not auto_submit:
            selected_option = self.var.get()
            if selected_option == "":
                messagebox.showwarning("Warning", "Please select an answer!")
                return
        else:
            selected_option = None

        correct_answer = self.questions[self.question_index]['answer']
        if selected_option == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            if auto_submit:
                messagebox.showinfo("Time's up!", f"Correct answer: {correct_answer}")
            else:
                messagebox.showinfo("Wrong!", f"Correct answer: {correct_answer}")

        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.question_index += 1
        if self.question_index >= len(self.questions):
            self.show_final_score()
        else:
            self.display_question()

    def show_final_score(self):
        messagebox.showinfo("Quiz Complete", f"Your final score is: {self.score}")
        name = simpledialog.askstring("Save Score", "Enter your name:")
        if name:
            self.save_score(name, self.score)
        self.display_high_scores()

    def save_score(self, name, score, filename='high_scores.txt'):
        try:
            with open(filename, 'a') as file:
                file.write(f"{name}: {score}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the score: {e}")

    def display_high_scores(self, filename='high_scores.txt'):
        self.clear_screen()
        tk.Label(self.root, text="High Scores", font=('Arial', 20)).pack(pady=20)

        try:
            with open(filename, 'r') as file:
                scores = file.readlines()
                for score in scores:
                    tk.Label(self.root, text=score.strip(), font=('Arial', 14)).pack(anchor='w', padx=10)
        except FileNotFoundError:
            tk.Label(self.root, text="No high scores yet.", font=('Arial', 14)).pack(pady=10)
        except Exception as e:
            tk.Label(self.root, text=f"Error loading high scores: {e}", font=('Arial', 14)).pack(pady=10)

        tk.Button(self.root, text="Play Again", command=self.start_quiz, font=('Arial', 14)).pack(pady=20)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=('Arial', 14)).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
