#Main auth script

from time import time_ns as nanos
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import json
import sys
import hashlib

def auth(name : str, password : str):
    data = {}
    with open('hashes.json', 'r') as f:
        data = json.loads(f.read())

    try:
        passwordHash = data[name]

        hasher = PasswordHasher()
        try:
            hasher.verify(passwordHash, password)
            token = hasher.hash(str(nanos()))
            return token
        except VerifyMismatchError:
            return 1
    except KeyError:
        return 1

def signUp(name, password):
    data = {}
    with open('hashes.json', 'r') as f:
        data = json.loads(f.read())

    try:
        exists_ = data[name]
        return 2
    except KeyError:
        pass

    common = {}
    with open('common.json', 'r') as f:
        common = json.loads(f.read())
    
    for pwd in common:
        if pwd == password:
            return 3

    hasher = PasswordHasher()
    data[name] = hasher.hash(password)

    with open('hashes.json', 'w') as f:
        json.dump(data, f)

    return 0

if __name__ == '__main__':
    sha256 = hashlib.sha256()
    sha256.update(bytes(sys.argv[2], encoding='utf8'))
    if sys.argv[3] == '0':
        print(str(auth(sys.argv[1], sha256.hexdigest())))
    else:
        print(str(signUp(sys.argv[1], sha256.hexdigest())))