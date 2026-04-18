from abc import ABC, abstractmethod
from user_module import UserInfo
from question_module import Question
import json
import csv


# This set a template for stroage classes
class Storage(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass


# This helps stores user infomation to storage
class UserInfoStorage(Storage):

    def __init__(self, filename):
        self.users_info = {}    # Stores user name as key and UserInfo object as value
        self.data = {}          # Stores file info from json file
        self.filename = filename


# Help upload json file infomation to memory
    def load(self):
        """ Upload JSON file infomation to memory """

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
    

    def save(self, current_user):
        """ Saves user information to storage """

        # Save current user info to data
        self.data[current_user.name] =  {
            "password": current_user.password, 
            "salt": current_user.salt, 
            "history": current_user.history, 
            "total_score": current_user.total_score
            }

        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4) # Save data to the specific filename


# This saves and load questions
class QuestionStorage(Storage):
    
    def __init__(self, filename): # Takes in filename
        self.filename = filename   

    def load(self):
        self.questions = []     # This holds questions as question object

        with open(self.filename) as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Create question object from question in CSV file and append it to questions
                self.questions.append(Question(row["Question"], row["Answer"]))
            return self.questions
    
   
    def save(self, questions):
        """ Add question to a CSV file """

        fieldname = ["Question", "Answer"]

        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldname)
            
            for question in questions:
                writer.writerow({"Question":question.text, "Answer": question.answer})

