#Mockup input script

from argon2 import PasswordHasher
import main

hasher = PasswordHasher()
name = input('name: ')
pwd = input('password: ')

auth = main.auth(name, pwd)

if auth[0]: #Authentication succedeed
    print("Logged in successfully. Token: " + auth[1])
else:
    print("Incorrect username or password.")