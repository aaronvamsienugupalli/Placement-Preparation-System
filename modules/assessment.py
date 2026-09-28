from modules.questions import QuestionBank
from utils.file_handler import load_json, save_json


class Assessment:

    def __init__(self, username):
        self.username = username
        self.question_bank = QuestionBank()
        self.questions = self.question_bank.get_all_questions()
        self.score = 0

    def start_test(self):
        print("\n===== PLACEMENT ASSESSMENT =====")

        for question in self.questions:

            print("\n" + question["question"])

            for i, option in enumerate(question["options"], start=1):
                print(f"{i}. {option}")

            try:
                choice = int(input("Enter your answer (1-4): "))

                if question["options"][choice - 1] == question["answer"]:
                    self.score += 1

            except (ValueError, IndexError):
                print("Invalid choice. Answer counted as incorrect.")

        print("\n===== TEST COMPLETED =====")
        print("Username:", self.username)
        print("Score:", self.score, "/", len(self.questions))

        self.save_result()

    def save_result(self):
        results_file = "data/results.json"

        results = load_json(results_file)

        results.append({
            "username": self.username,
            "score": self.score,
            "total_questions": len(self.questions)
        })

        save_json(results_file, results)

        print("Result saved successfully!")