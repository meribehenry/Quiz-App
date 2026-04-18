from storage_module import QuestionStorage, UserInfoStorage
from user_module import UserSystem
from quiz_module import QuizSystem
from CLI_module import CLIDisplayService, CLILoginService


def options():
    print("\n1. To register\n2. To login\n3. To start quiz\n4. To see past results\n5. To see options\n6. To exit")

QUESTION_FILE = "question.csv"
USER_INFO_FILE = "user_info.json"

valid_options = ["1", "2", "3", "4", "5", "6"]

def main():

    questions = QuestionStorage(QUESTION_FILE).load()
    info_storage = UserInfoStorage(USER_INFO_FILE)
    info_storage.load()
    users_info_dict = info_storage.users_info
    user_system = UserSystem(users_info_dict)
    quiz = QuizSystem(questions)
    quiz_display = CLIDisplayService()
    login_display = CLILoginService()

    options()
    current_user = ""

    while True:
        try:
            option = input("> ").strip()

            if option == "6":
                info_storage.save(current_user)
                print("Program closed")
                return None
            
            if option not in valid_options:
                print("Invalid option")
                continue

            if option == "5":
                options()
                continue
            
            if not current_user and option == "1":
                person = login_display.register_service(user_system)

                if person:
                    current_user = person
                    print(f"Successfully created an account")
                else:
                    print("Account creation failed")
            
            elif not current_user and option == "2":
                person = login_display.login_service(user_system)

                if person:
                    current_user = person
                    print(f"Successfully logged in")
                else:
                    print("Login failed")
                
                continue
                
            if current_user:
                if option == "3":
                    quiz_display.display_quiz(quiz, current_user)
                
                elif option == "4":
                    quiz_display.display_past_results(current_user)

            else:
                print("Login or Register first")

        except ValueError as e:
            print(f"Error! {e}")

            
if __name__ == "__main__":
    main()