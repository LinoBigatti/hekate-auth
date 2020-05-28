#Server handler

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json

import main

config = {}
with open('config.json', 'r') as f:
    config = json.load(f)
ip = config["ip"]
port = config["port"]
helpMessage = bytes(config["helpMessage"], encoding='utf-8')
key = config["key"]
cert = config["cert"]


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(helpMessage)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload_raw = self.rfile.read(content_length)
        print(payload_raw)
        payload = json.loads(payload_raw.decode('utf8'))
        op = int(payload["op"])
        try:
            if op >= 2:
                self.send_response(501)
                self.end_headers()
                self.wfile.write(b'Operation not found.\n')
                self.wfile.write(helpMessage)
                return
            else:
                pass
        except TypeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid payload.\n')
            self.wfile.write(helpMessage)
            return

        try:
            response = None
            if op == 0:
                response = main.auth(payload["name"], payload["password"])
            elif op == 1:
                response = main.signUp(payload["name"], payload["password"])
            else:
                self.send_response(501)
                self.end_headers()
                self.wfile.write(b'Operation not found.\n')
                self.wfile.write(helpMessage)
                return

            if response == 0:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Signed up successfully. Please sign in now.')
            elif response == 1:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Username or password incorrect.')
            elif response == 2:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'That name is already taken.')
            elif response == 3:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'The password cant be in the 10.000 most used passwords list.')
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Signed in successfully. Session token:\n')
                self.wfile.write(bytes(response, encoding='utf8'))
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Invalid payload.\n')
            self.wfile.write(helpMessage)
            return

server = HTTPServer((ip, port), requestHandler)
server.socket = ssl.wrap_socket(server.socket, keyfile=key, certfile=cert, server_side=True)

server.serve_forever()