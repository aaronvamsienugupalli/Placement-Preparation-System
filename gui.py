import tkinter as tk
from tkinter import messagebox

from modules.user import User
from modules.questions import QuestionBank
from utils.file_handler import load_json, save_json


class LoginGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Placement Preparation & Assessment System")
        self.root.geometry("600x500")

        self.username = ""
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.selected_answer = tk.IntVar()

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGIN SCREEN ----------------

    def show_login_screen(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Placement Preparation & Assessment System",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=30)

        username_label = tk.Label(
            self.root,
            text="Username",
            font=("Arial", 12)
        )
        username_label.pack()

        self.username_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=5)

        password_label = tk.Label(
            self.root,
            text="Password",
            font=("Arial", 12)
        )
        password_label.pack()

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 12),
            show="*"
        )
        self.password_entry.pack(pady=5)

        login_button = tk.Button(
            self.root,
            text="Login",
            width=15,
            command=self.login
        )
        login_button.pack(pady=15)

        register_button = tk.Button(
            self.root,
            text="Register",
            width=15,
            command=self.register
        )
        register_button.pack()

    # ---------------- LOGIN ----------------

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if User.login(username, password):
            self.username = username
            self.show_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    # ---------------- REGISTER ----------------

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )
            return

        if User.register(username, password):
            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully!"
            )
        else:
            messagebox.showerror(
                "Registration Failed",
                "Username already exists."
            )

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Dashboard",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=30)

        welcome = tk.Label(
            self.root,
            text=f"Welcome, {self.username}!",
            font=("Arial", 14)
        )
        welcome.pack(pady=10)

        info = tk.Label(
            self.root,
            text="Ready to begin your placement assessment?",
            font=("Arial", 11)
        )
        info.pack(pady=10)

        start_button = tk.Button(
            self.root,
            text="Start Assessment",
            width=20,
            height=2,
            command=self.start_assessment
        )
        start_button.pack(pady=20)

        results_button = tk.Button(
            self.root,
            text="View Results",
            width=20,
            height=2,
            command=self.view_results
        )
        results_button.pack(pady=10)

        logout_button = tk.Button(
            self.root,
            text="Logout",
            width=15,
            command=self.logout
        )
        logout_button.pack(pady=10)

    # ---------------- START ASSESSMENT ----------------

    def start_assessment(self):
        question_bank = QuestionBank()

        self.questions = question_bank.get_all_questions()

        if not self.questions:
            messagebox.showerror(
                "Error",
                "No questions available."
            )
            return

        self.current_question = 0
        self.score = 0

        self.show_question()

    # ---------------- QUESTION SCREEN ----------------

    def show_question(self):
        self.clear_screen()

        question = self.questions[self.current_question]

        title = tk.Label(
            self.root,
            text="Placement Assessment",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        progress = tk.Label(
            self.root,
            text=f"Question {self.current_question + 1} "
                 f"of {len(self.questions)}",
            font=("Arial", 11)
        )
        progress.pack(pady=5)

        question_label = tk.Label(
            self.root,
            text=question["question"],
            font=("Arial", 13, "bold"),
            wraplength=500,
            justify="left"
        )
        question_label.pack(pady=20)

        self.selected_answer.set(0)

        for index, option in enumerate(
            question["options"],
            start=1
        ):
            radio_button = tk.Radiobutton(
                self.root,
                text=option,
                variable=self.selected_answer,
                value=index,
                font=("Arial", 11),
                anchor="w",
                width=40
            )

            radio_button.pack(pady=5)

        if self.current_question == len(self.questions) - 1:

            next_button = tk.Button(
                self.root,
                text="Submit Test",
                width=15,
                command=self.submit_test
            )

        else:

            next_button = tk.Button(
                self.root,
                text="Next",
                width=15,
                command=self.next_question
            )

        next_button.pack(pady=25)

    # ---------------- NEXT QUESTION ----------------

    def next_question(self):

        if self.selected_answer.get() == 0:
            messagebox.showwarning(
                "Select Answer",
                "Please select an answer before continuing."
            )
            return

        question = self.questions[self.current_question]

        selected_index = self.selected_answer.get() - 1

        selected_option = question["options"][selected_index]

        if selected_option == question["answer"]:
            self.score += 1

        self.current_question += 1

        self.show_question()

    # ---------------- SUBMIT TEST ----------------

    def submit_test(self):

        if self.selected_answer.get() == 0:
            messagebox.showwarning(
                "Select Answer",
                "Please select an answer before submitting."
            )
            return

        question = self.questions[self.current_question]

        selected_index = self.selected_answer.get() - 1

        selected_option = question["options"][selected_index]

        if selected_option == question["answer"]:
            self.score += 1

        self.show_result()

    # ---------------- RESULT ----------------

    def show_result(self):
        self.save_result()

        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Assessment Completed!",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=30)

        score_label = tk.Label(
            self.root,
            text=f"Your Score: {self.score} / {len(self.questions)}",
            font=("Arial", 16)
        )
        score_label.pack(pady=20)

        dashboard_button = tk.Button(
            self.root,
            text="Back to Dashboard",
            width=20,
            command=self.show_dashboard
        )
        dashboard_button.pack(pady=10)

        logout_button = tk.Button(
            self.root,
            text="Logout",
            width=15,
            command=self.logout
        )
        logout_button.pack(pady=10)

    # ---------------- SAVE RESULT ----------------

    def save_result(self):
        results_file = "data/results.json"

        results = load_json(results_file)

        results.append({
            "username": self.username,
            "score": self.score,
            "total_questions": len(self.questions)
        })

        save_json(results_file, results)

    # ---------------- VIEW RESULTS ----------------

    def view_results(self):
        results_file = "data/results.json"

        results = load_json(results_file)

        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Assessment Results",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=25)

        user_results = [
            result for result in results
            if result["username"] == self.username
        ]

        if not user_results:

            message = tk.Label(
                self.root,
                text="No assessment results found.",
                font=("Arial", 12)
            )
            message.pack(pady=20)

        else:

            for index, result in enumerate(
                user_results,
                start=1
            ):
                result_text = (
                    f"Test {index}: "
                    f"{result['score']} / "
                    f"{result['total_questions']}"
                )

                result_label = tk.Label(
                    self.root,
                    text=result_text,
                    font=("Arial", 12)
                )
                result_label.pack(pady=5)

        back_button = tk.Button(
            self.root,
            text="Back to Dashboard",
            width=20,
            command=self.show_dashboard
        )
        back_button.pack(pady=20)

    # ---------------- LOGOUT ----------------

    def logout(self):
        self.username = ""
        self.questions = []
        self.current_question = 0
        self.score = 0

        self.show_login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    root.mainloop()