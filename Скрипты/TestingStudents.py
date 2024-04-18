import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Тест")
        self.questions = []
        self.answers = []
        self.testkey = [1, 0, 3, 1, 2, 0, 2, 1, 1, 3, 2, 0, 2, 1, 3, 0, 3, 2, 0, 1, 0, 2, 3, 1, 2]
        self.load_questions_and_answers("questions.txt")
        self.current_question_index = 0
        self.max_score = len(self.testkey)
        self.score = 0

        self.question_label = tk.Label(master, text="")
        self.question_label.pack()

        self.buttons = []
        for i in range(4):
            button = tk.Button(master, text="", width=30, command=lambda i=i: self.check_answer(i))
            button.pack(pady=5)
            self.buttons.append(button)

        self.display_question()

    def load_questions_and_answers(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 6):
                question = lines[i].strip()
                self.questions.append(question)
                answers = [line.strip()[3:] for line in lines[i + 1:i + 5]]
                self.answers.append(answers)

    def display_question(self):
        question = self.questions[self.current_question_index]
        self.question_label.config(text=question)
        answers = self.answers[self.current_question_index]
        for i in range(4):
            self.buttons[i].config(text=answers[i])

    def check_answer(self, selected_index):
        correct_answer_index = self.testkey[self.current_question_index]
        if selected_index == correct_answer_index:
            self.score += 1
            messagebox.showinfo("Результат", "Верно!")
        else:
            messagebox.showerror("Результат", "Неверно!")
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        messagebox.showinfo("Результат", f"Тест завершен.\nМаксимальный балл: {self.max_score}\nПолучено баллов: {self.score}")

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
