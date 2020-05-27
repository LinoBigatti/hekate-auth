#Main auth script

from time import time_ns as nanos
from argon2 import PasswordHasher
import json

def auth(name, password):
    data = {}
    with open('hashes.json', 'r') as f:
        data = json.loads(f.read())

    try:
        passwordHash = data[name]

        hasher = PasswordHasher()
        if hasher.verify(passwordHash, password):
            token = hasher.hash(str(nanos()))
            return [True, token]
        else:
            return[False, None]
    except KeyError:
        return [False, None]

def signUp(name, password):
    data = {}
    with open('hashes.json', 'r') as f:
        data = json.loads(f.read())

    try:
        exists_ = data[name]
        return 1
    except KeyError:
        pass

    common = {}
    with open('common.json', 'r') as f:
        common = json.loads(f.read())
    
    for pwd in common:
        if pwd == password:
            return 2

    hasher = PasswordHasher()
    data[name] = hasher.hash(password)

    with open('hashes.json', 'w') as f:
        json.dump(data, f)

    return 0