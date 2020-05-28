#Mockup input script

import hashlib
import requests
import json
import urllib3
urllib3.disable_warnings()

config = {}
with open('config.json', 'r') as f:
    config = json.load(f)
ip = 'https://' + config["ip"] if config["ip"] != 'localhost' else 'https://127.0.0.1'
ip += ':' + str(config["port"]) + '/'
cert = config["cert"]

print("ip: " + ip)

sha256 = hashlib.sha256()
name = input('name: ')
sha256.update(bytes(input("password: "), encoding='utf8'))
pwd = sha256.hexdigest()

data1 = b'{"op": '
data2 = bytes(', "name": "' + name + '", "password": "' + pwd + '"}', encoding='utf8')

#client = http.client.HTTPSConnection(ip, 4443, verify='certs/cert.pem')

while True:
    r = None

    op = input("Operation: (signin/signup/get/exit) ")
    if op == "signin":
        r = requests.post(ip, data=data1 + b'0' + data2 ,verify=cert)
    elif op == "signup":
        r = requests.post(ip, data=data1 + b'1' + data2 ,verify=cert)
    elif op == "get":
        r = requests.get(ip, verify='certs/cert.pem')
    elif op == "exit":
        exit()

    print(r)
    print(r.text)