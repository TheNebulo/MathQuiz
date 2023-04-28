import random
import json
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog

class MathTestApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Math Quiz")
        self.geometry("400x300")

        self.valid_class_names = ['Class A', 'Class B', 'Class C']
        self.valid_difficulties = ['Easy', 'Medium', 'Hard']

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text="Main Menu", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(self.main_frame, text="Take the Quiz", command=self.take_test, width=15).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="View High Scores", command=self.view_high_scores, width=15).grid(row=1, column=1, pady=5)
        tk.Button(self.main_frame, text="Teacher Menu", command=self.teacher_auth, width=15).grid(row=2, column=0, pady=5)
        tk.Button(self.main_frame, text="Exit", command=self.quit, width=15).grid(row=2, column=1, pady=5)

    def teacher_auth(self):
        password = "teacher123"
        entered_password = tk.simpledialog.askstring("Teacher Menu", "Enter teacher password:", show='*')
        if entered_password == password:
            self.teacher_menu()
        elif entered_password != None:
            messagebox.showerror("Error", "Invalid password. Please try again.")

    def generate_question(self, difficulty):
        difficulties = {
            "Easy": (1, 10),
            "Medium": (1, 20),
            "Hard": (1, 100)
        }
        lower, upper = difficulties[difficulty]
        num1 = random.randint(lower, upper)
        num2 = random.randint(lower, upper)
        operation = random.choice(['+', '-', '*', '/'])
        if operation == '/':
            num1 *= num2
        question = f"{num1} {operation} {num2}"
        return question

    def save_results(self, class_name, student_name, score, difficulty):
        if not os.path.exists('results'):
            os.makedirs('results')
        file_name = os.path.join('results', f'{class_name}.json')
        data = {}
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                data = json.load(file)
        if student_name not in data:
            data[student_name] = []
        data[student_name].append({"score": score, "difficulty": difficulty})
        data[student_name] = data[student_name][-3:]
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def take_test(self):
        top_level = tk.Toplevel(self)
        test_app = TestApp(top_level, self)
        test_app.pack()

    def view_high_scores(self):
        top_level = tk.Toplevel(self)
        high_scores_app = HighScoresApp(top_level, self)
        high_scores_app.pack()

    def teacher_menu(self):
        top_level = tk.Toplevel(self)
        teacher_menu_app = TeacherMenuApp(top_level, self)
        teacher_menu_app.pack()
        
    def check_answer(self, question, given_answer):
        try:
            correct_answer = eval(question)
        except ZeroDivisionError:
            return False

        return round(correct_answer, 2) == round(given_answer, 2)


class TestApp(tk.Frame):

    def __init__(self, master, root_app):
        super().__init__(master)

        self.master.title("Take the Quiz")
        self.master.geometry("400x300")

        self.root_app = root_app

        self.create_widgets()
        
    def create_widgets(self):
        self.current_question = 0

        self.intro_frame = tk.Frame(self)
        self.intro_frame.pack(pady=20)

        self.test_class_label = tk.Label(self.intro_frame, text="Enter Class Name:")
        self.test_class_label.grid(row=0, column=0)

        self.test_class_var = tk.StringVar()
        self.test_class_var.set("Class A")
        self.test_class_menu = tk.OptionMenu(self.intro_frame, self.test_class_var, *self.root_app.valid_class_names)
        self.test_class_menu.grid(row=0, column=1)

        self.difficulty_label = tk.Label(self.intro_frame, text="Select Difficulty:")
        self.difficulty_label.grid(row=1, column=0)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Easy")
        self.difficulty_menu = tk.OptionMenu(self.intro_frame, self.difficulty_var, *self.root_app.valid_difficulties)
        self.difficulty_menu.grid(row=1, column=1)

        self.student_name_label = tk.Label(self.intro_frame, text="Enter Student Name:")
        self.student_name_label.grid(row=2, column=0)

        self.student_name_var = tk.StringVar()
        self.student_name_entry = tk.Entry(self.intro_frame, textvariable=self.student_name_var)
        self.student_name_entry.grid(row=2, column=1)

        self.start_test_button = tk.Button(self.intro_frame, text="Start Quiz", command=self.start_test)
        self.start_test_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.test_frame = tk.Frame(self)

        self.question_label = tk.Label(self.test_frame, text="Question:")
        self.question_label.grid(row=0, column=0)

        self.question_text = tk.StringVar()
        self.question = tk.Label(self.test_frame, textvariable=self.question_text, font=("Arial", 18))
        self.question.grid(row=1, column=0, columnspan=2, pady=10)

        self.answer_label = tk.Label(self.test_frame, text="Your Answer:")
        self.answer_label.grid(row=2, column=0)

        self.answer_var = tk.DoubleVar()
        self.answer_entry = tk.Entry(self.test_frame, textvariable=self.answer_var)
        self.answer_entry.grid(row=2, column=1)

        self.next_question_button = tk.Button(self.test_frame, text="Next Question", command=self.check_and_next_question)
        self.next_question_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.score = 0

    def start_test(self):
        self.intro_frame.pack_forget()
        self.test_frame.pack(pady=20)

        self.class_name = self.test_class_var.get()
        self.difficulty = self.difficulty_var.get()
        self.student_name = self.student_name_var.get()

        if not self.student_name.strip():
            messagebox.showerror("Error", "Please enter a student name.")
            return

        self.current_question = 0
        self.get_next_question()
        
    def get_next_question(self):
        self.current_question += 1
        if self.current_question <= 10:
            self.quest = self.root_app.generate_question(self.difficulty)
            self.question_text.set(self.quest)
            self.answer_var.set(0)
        else:
            self.show_results()
            
    def check_and_next_question(self):
        try:
            answer = self.answer_var.get()
            if self.root_app.check_answer(self.quest, answer):
                self.score += 1
        except:
            pass
        self.get_next_question()
        
    def show_results(self):
        self.test_frame.pack_forget()
        
        self.result_label = tk.Label(self, text=f"{self.student_name} got {self.score} out of 10.")
        self.result_label.pack(pady=20)

        self.root_app.save_results(self.class_name, self.student_name, self.score, self.difficulty)

        self.quit_button = tk.Button(self, text="Close", command=self.master.destroy)
        self.quit_button.pack(pady=10)
        

class HighScoresApp(tk.Frame):

    def __init__(self, master, root_app):
        super().__init__(master)

        self.master.title("High Scores")
        self.master.geometry("400x300")

        self.root_app = root_app

        self.create_widgets()

    def create_widgets(self):
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=20)

        self.results_text = tk.Text(self.result_frame, width=40, height=12)
        self.results_text.pack()

        self.show_results()

        self.close_button = tk.Button(self, text="Close", command=self.master.destroy)
        self.close_button.pack(pady=10)

    def show_results(self):
        result_text = ""
        for class_name in self.root_app.valid_class_names:
            file_name = os.path.join('results', f'{class_name}.json')
            if os.path.exists(file_name):
                with open(file_name, 'r') as file:
                    data = json.load(file)
                sorted_data = sorted(data.items(), key=lambda x: (-max([d["score"] for d in x[1]]), x[0]))
                result_text += f"\nHigh scores for {class_name}:\n"
                for student, scores in sorted_data:
                    highest_score = max(scores, key=lambda x: x['score'])
                    result_text += f"{student}: {highest_score['score']} ({highest_score['difficulty']})\n"
            else:
                result_text += f"No data for {class_name}\n"
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.INSERT, result_text)

class TeacherMenuApp(tk.Frame):

    def __init__(self, master, root_app):
        super().__init__(master)

        self.master.title("Teacher Menu")
        self.master.geometry("400x300")

        self.root_app = root_app

        self.create_widgets()

    def create_widgets(self):
        self.class_label = tk.Label(self, text="Select Class:")
        self.class_label.pack(pady=10)

        self.class_var = tk.StringVar()
        self.class_var.set("Class A")
        self.class_menu = tk.OptionMenu(self, self.class_var, *self.root_app.valid_class_names)
        self.class_menu.pack()

        self.view_results_button = tk.Button(self, text="View Results", command=self.view_results)
        self.view_results_button.pack(pady=10)

        self.results_frame = tk.Frame(self)
        self.results_frame.pack(pady=20)

        self.results_text = tk.Text(self.results_frame, width=40, height=12)
        self.results_text.pack()

        self.close_button = tk.Button(self, text="Close", command=self.master.destroy)
        self.close_button.pack(pady=10)

    def view_results(self):
        class_name = self.class_var.get()

        file_name = os.path.join('results', f'{class_name}.json')
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                data = json.load(file)
            sorted_data = sorted(data.items(), key=lambda x: (-max([d["score"] for d in x[1]]), x[0]))
            result_text = f"\nResults for {class_name}:\n"
            for student, scores in sorted_data:
                scores_text = ', '.join([f"{score_data['score']} ({score_data['difficulty']})" for score_data in scores])
                result_text += f"{student}: {scores_text}\n"
        else:
            result_text = f"No data for {class_name}\n"
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.INSERT, result_text)


if __name__ == "__main__":
    app = MathTestApp()
    app.mainloop()
