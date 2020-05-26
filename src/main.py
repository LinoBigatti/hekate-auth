#Main auth script

from time import time_ns as nanos
from argon2 import PasswordHasher
import json

def auth(name, password):
    data = {}
    with open('shas.json', 'r') as f:
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
    pass