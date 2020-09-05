#Mockup input script

import hashlib
import requests
import json
import urllib3
urllib3.disable_warnings()  #Disable urllib warnings

config = {}     #Load configuration.
with open('config.json', 'r') as f:
    config = json.load(f)
#Configure ip
ip = 'https://' + config["ip"] if config["ip"] != 'localhost' else 'https://127.0.0.1'
ip += ':' + str(config["port"]) + '/'
#Get certificate
cert = config["cert"]

print("ip: " + ip)

sha256 = hashlib.sha256()   #Start a hasher
name = input('name: ')      #Get the name
email = input('email: ')    #Get the email
sha256.update(bytes(input("password: "), encoding='utf8'))
pwd = sha256.hexdigest()    #Hash the password

#Payload
data1 = b'{"op": '
data2 = bytes(', "name": "' + name + '", "password": "' + pwd + ', "email": "' + email + '" }', encoding='utf8')

while True:     #Command handler
    r = None

    op = input("Operation: (signin/signup/get/exit) ")
    if op == "signin":  #Send a POST to sign in
        r = requests.post(ip, data=data1 + b'0' + data2 ,verify=cert)
    elif op == "signup":    #Send a POST to sign up
        r = requests.post(ip, data=data1 + b'1' + data2 ,verify=cert)
    elif op == "get":   #Send a GET
        r = requests.get(ip, verify=cert)
    elif op == "exit":  #Exit
        exit()

    print(r)
    print(r.text)