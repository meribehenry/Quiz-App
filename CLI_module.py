# This helps with the CLI display
class CLIDisplayService:

    def display_quiz(self, quiz, current_user):
        """ Handles the display of quiz in the terminal"""
        quiz.start_quiz()

        while not quiz.is_finished():
            question = quiz.get_question()
            print(f"{quiz.current_index + 1}. {question.text}")
            answer = input("Answer: ").strip()
            quiz.submit_answer(answer)
        quiz.update_record(current_user)
        
        print("\n         <<<<< YOUR ANSWERS >>>>>        ")
        for index, (question, answer) in enumerate(quiz.user_answers, start=1):
            print(f"{index}. {question.text.capitalize()}: {answer.capitalize()}")
    
        print("\n         <<<<< CORRECT ANSWERS >>>>>        ")
        for index, question in enumerate(quiz.questions, start=1):
            print(f"{index}. {question.text.capitalize()}: {question.answer.capitalize()}")
        
        print(f"Your score: {quiz.score}/{len(quiz.questions)}")
    

    def display_past_results(self, current_user):
        """ Handles the display of history in the terminal"""

        for date, info in current_user.history.items():
            print(f"\n        <<<<< ON {date} >>>>>")
            for index, (question, answer) in enumerate(info["question"].items(), start=1):
                print(f"{index}. {question}: {answer.capitalize()}")
            print(f"Score: {info['score']}/{len(info['question'])}")
        print(f"\nTotal Score: {current_user.total_score}")


# This helps with the Login service on the CLI
class CLILoginService:

    def register_service(self, user_system):
        """ Handles the display of registering process in the terminal"""

        name = input("Enter name: ").strip()
        password = input("Enter password: ").strip()

        if user_system.register(name, password):
            return user_system.current_user

    def login_service(self, user_system):
        """ Handles the display of logging in process in the terminal"""

        name = input("Enter name: ").strip()
        password = input("Enter password: ").strip()

        if user_system.login(name, password):
            return user_system.current_user