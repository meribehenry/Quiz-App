from collections import defaultdict
import os
import hashlib
from datetime import datetime
import json
from abc import ABC, abstractmethod
import csv


# This set a template for stroage classes
class Storage(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass


# This help to create user information object
class UserInfo:
    def __init__(self, name, password, salt, history, total_score):
        self.name = name
        self.__password = password     
        self.__salt = salt
        self.history = history
        self.__total_score = total_score

    @property
    def password(self):
        return self.__password
    
    @property
    def salt(self):
        return self.__salt
        
    @property
    def total_score(self):
        return self.__total_score

    @total_score.setter
    def total_score(self, score):
        if score < 0:
            raise ValueError("Score must be positive")

        self.__total_score = score


# This helps stores user infomation to storage
class UserInfoStorage(Storage):

    def __init__(self, filename):
        self.users_info = {}    # Stores user name as key and UserInfo object as value
        self.data = {}          # Stores file info from json file
        self.filename = filename


# Help upload json file infomation to memory
    def load(self):
        try:
            with open(self.filename) as file:
                self.data = json.load(file)
               
               # Loop through users data and create UserInfo object
                for name, info in self.data.items():
                    password = info["password"]
                    salt = info["salt"]
                    history = info["history"]

                    total_score = info.get("total_score", 0)

                    # Stores user name and UserInfo object to users_info attribute
                    self.users_info[name] = UserInfo(name, password, salt, history, total_score)

        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
# Helps to save user information to storage
    def save(self, current_user):
        
        # Save current user info to data
        self.data[current_user.name] =  {
            "password": current_user.password, 
            "salt": current_user.salt, 
            "history": current_user.history, 
            "total_score": current_user.total_score
            }

        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4) # Save data to the specific filename

    
# This handles all the register and login logic
class UserSystem:
    def __init__(self, users):
        self.users = users  # This holds dictionary of key (name) and value (user object)
    
    def register(self, name, password):
        if name in self.users:
            raise ValueError("Name already exist")
        
        salt = os.urandom(16)   # Generates salt 
        hashed_password = hashlib.sha256(salt + password.encode()).hexdigest() # Encrypts user password
        
        # Create UserInfo object as current user
        self.current_user = UserInfo(name, hashed_password, salt.hex(), history=defaultdict(dict), total_score=0)

        return True

    def login(self, name, password):
        if name not in self.users:
            raise ValueError("Name does not exist")

        stored_salt = bytes.fromhex(self.users[name].salt)  # Gets user stored salt
        stored_password = self.users[name].password         # Gets user stored password
        unchecked_password = hashlib.sha256(stored_salt + password.encode()).hexdigest() 

        # Validate password
        if stored_password == unchecked_password:
            self.current_user = self.users[name]
            return True
        
        return False


# This helps to store questions
class Question:
    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

# Checks if user answer matches the correct answer
    def is_correct(self, user_answer):
        return self.answer.lower() == user_answer.lower()
    

# This saves and load question
class QuestionStorage(Storage):
    
    def __init__(self, filename): # Takes in filename
        self.filename = filename   

    def load(self):
        self.questions = []     # This holds questions as question object

        with open(self.filename) as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Create question object from question in file and append it to questions
                self.questions.append(Question(row["Question"], row["Answer"]))
            return self.questions

# Add question to file   
    def save(self, questions):
        fieldname = ["Question", "Answer"]

        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldname)
            
            for question in questions:
                writer.writerow({"Question":question.text, "Answer": question.answer})


# Helps with the quiz logic
class QuizSystem:

    def __init__(self, questions):  # Takes in list of question object
        self.questions = questions
        self.__user_answers = []
        self.__score = 0
    
    def start_quiz(self):
        # Reset all previous history  
        self.__user_answers = []
        self.current_index = 0
        self.__score = 0
    
    def get_question(self):
        return self.questions[self.current_index] # Return question in order
    
    def submit_answer(self, answer):
        question = self.questions[self.current_index]
        self.__user_answers.append((question, answer)) # Store question object and user answer to user_answers

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


# This helps with the CLI display
class CLIDisplayService:

    def display_quiz(self, quiz, current_user):
        quiz.start_quiz()

        while not quiz.is_finished():
            question = quiz.get_question()
            print(f"{question.text}")
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
        for date, info in current_user.history.items():
            print(f"\n        <<<<< ON {date} >>>>>")
            for index, (question, answer) in enumerate(info["question"].items(), start=1):
                print(f"{index}. {question}: {answer}")
            print(f"Score: {info['score']}/{len(info['question'])}")
        print(f"\nTotal Score: {current_user.total_score}")


# This helps with the Login service on the CLI
class CLILoginService:

    def register_service(self, user_system):
        name = input("Enter name: ").strip()
        password = input("Enter password: ").strip()

        if user_system.register(name, password):
            return user_system.current_user

    def login_service(self, user_system):
        name = input("Enter name: ").strip()
        password = input("Enter password: ").strip()

        if user_system.login(name, password):
            return user_system.current_user
        
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

