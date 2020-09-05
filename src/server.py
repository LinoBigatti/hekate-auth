#Server handler

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json

import main

config = {}     #Load configuration values
with open('config.json', 'r') as f:
    config = json.load(f)
ip = config["ip"]
port = config["port"]
helpMessage = bytes(config["helpMessage"], encoding='utf-8')
key = config["key"]
cert = config["cert"]

class requestHandler(BaseHTTPRequestHandler):   #Main request handler
    def do_GET(self):   #GET request: Send help message
        self.sendHelp(200, '')

    def do_POST(self):  #POST request: Relay it to auth script
        content_length = int(self.headers['Content-Length'])

        #Get the payload
        payload_raw = self.rfile.read(content_length)
        payload = json.loads(payload_raw.decode('utf8'))

        try:    #Get the operation number
            op = int(payload["op"])
        except TypeError:   #NaN, inform the requester and send help message
            self.sendHelp(400, 'Invalid payload.\n')
            return

        try:
            response = None
            if op == 0:     #Authenticate
                response = main.auth(payload["email"], payload["password"])
            elif op == 1:   #Sign up
                response = main.signUp(payload["name"], payload["password"], payload["email"])
            else:           #Invalid operation
                self.sendHelp(501,  'Operation not found.\n')
                return

            if response == 0:   #Signed up correctly
                self.send(200, 'Signed up successfully. Please sign in now.')
            elif response == 1: #Authentication error
                self.send(403, 'Email or password incorrect.')
            elif response == 2: #Email is taken
                self.send(403, 'That email is already taken.')
            elif response == 3: #Password is too common
                self.send(403, 'The password cant be in the 10.000 most used passwords list.')
            elif response == 4: #Token is wrong
                self.send(403, 'Token is incorrect. Please log out and log in again.')
            else:               #Authenticated correctly
                self.send(200, response)
        except Exception as e:  #??? I dont even know why I put this in
            self.sendHelp(400, 'Invalid payload.\n')
            print("Error encountered: " + str(e))
            return

    def send(self, code, message):  #Send a message
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf8'))

    def sendHelp(self, code, message):  #Send a help message
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf8'))
        self.wfile.write(helpMessage)

server = HTTPServer((ip, port), requestHandler) #Create an http server

#Create a secure connection through ssl
server.socket = ssl.wrap_socket(server.socket, keyfile=key, certfile=cert, server_side=True)

server.serve_forever()  #Turn on server