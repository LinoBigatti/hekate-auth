#Mockup input script

import main
import hashlib

sha256 = hashlib.sha256()
name = input('name: ')
sha256.update(bytes(input("password: "), encoding='utf8'))
pwd = sha256.hexdigest()

while True:
    op = input("Operation: (signin/signup/exit) ")
    if op == "signin":
        auth = main.auth(name, pwd)
        if auth[0]: #Authentication succedeed
            print("Logged in successfully. Token: " + auth[1])
        else:
            print("Incorrect username or password.")
    elif op == "signup":
        code = main.signUp(name, pwd)
        if code == 0:
            print("Signed up successfully. Please sign in now.")
        elif code == 1:
            print("That name is already taken.")
        elif code == 2:
            print("The password must not be in the 10000 most used passwords list.")
    elif op == "exit":
        exit()