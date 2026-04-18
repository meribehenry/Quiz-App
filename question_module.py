# This helps to store questions
class Question:
    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

# Checks if user answer matches the correct answer
    def is_correct(self, user_answer):
        return self.answer.lower() == user_answer.lower()