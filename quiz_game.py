import tkinter as tk
import json
import os

# Load questions
file_path = os.path.join(os.path.dirname(__file__), "questions.json")

with open(file_path, "r") as file:
    questions = json.load(file)

current_question = 0
score = 0

def show_question():
    global current_question

    if current_question < len(questions):
        q = questions[current_question]

        question_label.config(text=q["question"])

        for i in range(len(options)):
            options[i].config(text=q["options"][i], value=q["options"][i])
    else:
        question_label.config(text=f"Quiz Finished! Your score: {score}")
        for option in options:
            option.destroy()
        submit_button.destroy()

def check_answer():
    global current_question, score

    selected = selected_option.get()

    if selected == questions[current_question]["answer"]:
        score += 1

    current_question += 1
    selected_option.set(None)

    show_question()

# GUI
root = tk.Tk()
root.title("Quiz Game")

question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
question_label.pack(pady=20)

selected_option = tk.StringVar()

options = []
for i in range(4):
    btn = tk.Radiobutton(root, text="", variable=selected_option, value="", font=("Arial", 12))
    btn.pack(anchor="w")
    options.append(btn)

submit_button = tk.Button(root, text="Next", command=check_answer)
submit_button.pack(pady=20)

show_question()

root.mainloop()