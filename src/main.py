#Main auth script

from time import time_ns as nanos
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import json
import sys
import hashlib
import os.path as path
import mongo

common = {}     #Load the 10.000 most common passwords list
with open('common.json', 'r') as f:
    common = json.loads(f.read())

#Sign in
def auth(email : str, password : str):
    user = mongo.findUser(email)

    if user:
        if user.verify(password):
            return str(user.jwt())
        else:           #Incorrect password
            return 1    #Incorrect user or password
    else:               #Incorrect user
        return 1        #Incorrect user or password

#Sign up
def signUp(name, password, email):
    for pwd in common:  #Check every common password
        if pwd == password: #If the password inputted is common, don't accept it
            return 3    #Password is too common

    hasher = PasswordHasher()
    pwd = hasher.hash(password)  #Hash the password using argon2

    user = mongo.user(name, pwd, email) #Generate an user
    if user.save() == 1:    #Email taken
        return 2

    return 0    #Success

if __name__ == '__main__':  #Handle being called directly
    sha256 = hashlib.sha256()
    sha256.update(bytes(sys.argv[2], encoding='utf8'))
    if sys.argv[3] == '0':  #Sign in
        print(str(auth(sys.argv[1], sha256.hexdigest())))
    else:                   #Sign up
        print(str(signUp(sys.argv[1], sha256.hexdigest())))