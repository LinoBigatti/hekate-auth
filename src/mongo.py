#Manage mongodb

import pymongo
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["auth"]
users = db["users"]

class user(object):
    def __init__(self, name, pwd, email):
        self.name = name
        self.pwd = pwd
        self.email = email
        self.permissions = 0    #Normal user

    def setPermissions(self, permissions):
        self.permissions = permissions

    def verify(self, password):
        hasher = PasswordHasher()
        try:

            hasher.verify(self.pwd, password)   #Verify the password

            return True
        except VerifyMismatchError:     #Incorrect password
            return False

    def jwt(self):
        key = 'secret'  #Note to self: change this

        payload = {}
        payload["name"] = self.name
        payload["id"] = str(users.find_one({"email": self.email})["_id"])
        payload["op"] = self.permissions

        return jwt.encode(payload, key, algorithm='HS256')

    def save(self):
        data = {}
        data["name"] = self.name
        data["pwd"] = self.pwd
        data["email"] = self.email
        data["op"] = self.permissions

        try:
            users.insert(data)
        except pymongo.errors.DuplicateKeyError:
            return 1

def findUser(email):
    data = users.find_one({"email": email})

    if data:
        found = user(data["name"], data["pwd"], data["email"])
        found.setPermissions(data["op"])

        return found
    
    return None