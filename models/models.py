from flask_login import UserMixin
from sqlalchemy import Column, Integer, String 

class User(UserMixin):
    id = int
    username = ""
    password_hash = ""

def isAuthenticated(self):
    return True
def isActive(self):
    return True
def isAnonymous(self):
    return False
def get_id(self):
    return str(self.id)
