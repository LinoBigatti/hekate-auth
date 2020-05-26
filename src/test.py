#Mockup input script

import main

name = input('name: ')
pwd = input('password: ')

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
    elif op == "exit":
        exit()