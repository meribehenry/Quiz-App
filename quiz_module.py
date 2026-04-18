from datetime import datetime


# Handles quiz logic
class QuizSystem:

    def __init__(self, questions):  # Takes in list of question object
        self.questions = questions
        self.__user_answers = []
        self.__score = 0
    
    def start_quiz(self):
        # Reset all previous quiz history  
        self.__user_answers = []
        self.current_index = 0
        self.__score = 0
    
    def get_question(self):
        return self.questions[self.current_index] # Return question from list in order
    
    def submit_answer(self, answer):
        question = self.questions[self.current_index]
        self.__user_answers.append((question, answer)) # Store question object and user answer to user_answers as a tuple

        if question.is_correct(answer):
            self.__score += 1

        self.current_index += 1 
    
    def update_record(self, current_user):
        quiz_questions = {}
        for question, answer in self.user_answers:
            quiz_questions[question.text] = answer

        current_user.total_score = current_user.total_score + self.__score
        current_user.history[str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))] = {"question": quiz_questions, "score": self.__score}
    
    def is_finished(self):        
        return self.current_index == len(self.questions)


    @property
    def score(self):
        return self.__score

    @property
    def user_answers(self):
        return self.__user_answers