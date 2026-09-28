from utils.file_handler import load_json


class QuestionBank:

    def __init__(self):
        self.questions_file = "data/questions.json"
        self.questions = load_json(self.questions_file)

    def get_all_questions(self):
        return self.questions

    def display_questions(self):
        for question in self.questions:
            print("\nQuestion:", question["question"])

            for i, option in enumerate(question["options"], start=1):
                print(f"{i}. {option}")

            print("Answer:", question["answer"])