from collections import defaultdict
import hashlib
import os


# Create user information object
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