#Main auth script

from time import time_ns as nanos
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import json
import sys
import hashlib

common = {}     #Load the 10.000 most common passwords list (Hashed with sha256)
with open('common.json', 'r') as f:
    common = json.loads(f.read())

#Sign in
def auth(name : str, password : str):
    data = {}   #Load the user data
    with open('hashes.json', 'r') as f:
        data = json.loads(f.read())

    try:    #Try to get the data for a given name
        passwordHash = data[name]

        hasher = PasswordHasher()
        try:
            hasher.verify(passwordHash, password)   #Verify the password

            token = hasher.hash(str(nanos()))[30:]  #Generate a unique token
            return token    #Send the token
        except VerifyMismatchError: #Incorrect password
            return 1    #Incorrect user or password
    except KeyError:    #Incorrect user
        return 1        #Incorrect user or password

#Sign up
def signUp(name, password):
    data = {}   #Load the user data
    with open('hashes.json', 'r') as f:
        data = json.loads(f.read())

    try:    #See if the username exists
        exists_ = data[name]
        return 2    #Username taken
    except KeyError:
        pass
    
    for pwd in common:  #Check every common password
        if pwd == password: #If the password inputted is common, don't accept it
            return 3    #Password is too common

    hasher = PasswordHasher()
    data[name] = hasher.hash(password)  #Rehash the password using argon2

    with open('hashes.json', 'w') as f: #Save the list
        json.dump(data, f)

    return 0    #Success

if __name__ == '__main__':  #Handle being called directly
    sha256 = hashlib.sha256()
    sha256.update(bytes(sys.argv[2], encoding='utf8'))
    if sys.argv[3] == '0':  #Sign in
        print(str(auth(sys.argv[1], sha256.hexdigest())))
    else:                   #Sign up
        print(str(signUp(sys.argv[1], sha256.hexdigest())))