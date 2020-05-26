#Main auth script

from time import time_ns as nanos
from argon2 import PasswordHasher
import json

hasher = PasswordHasher()

def auth(name, password):
    data = {}
    with open('shas.json', 'r') as f:
        data = json.loads(f.read())

    try:
        passwordHash = data[name]

        if hasher.verify(passwordHash, password):
            token = hasher.hash(str(nanos()))
            return [True, token]
        else:
            return[False, None]
    except KeyError:
        return [False, None]

def signUp(name, password):
    data = {}
    with open('shas.json', 'r') as f:
        data = json.loads(f.read())

    try:
        exists_ = data[name]
        return 1
    except KeyError:
        pass

    data[name] = hasher.hash(password)

    with open('shas.json', 'w') as f:
        json.dump(data, f)

    return 0