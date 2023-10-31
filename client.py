import socket
import threading
import json
from typing import Tuple

from logger import Logger
from message import Request, Response
from server import Address
from user import User

class Client:
    def __init__(self, ip, port, username, server_address: Address):
        self.user = User(username, ip, port)
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(90)
    
    def connect(self, address: Address):
        try:
            self.socket.connect((address.ip, int(address.port)))
            Logger.debug(f"Successful connection to: {address}")
        except socket.error as e:
            Logger.debug(f"Unsuccessful connection to: {address}")
            Logger.debug(e)

    def find_user(self, user: User):
        message = { 'username': user.username, 'op': 1, 'ip': user.ip, 'port': '' }
        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def signin(self):
        message = { 'username': self.user.username, 'op': 2, 'ip': self.user.ip, 'port': self.user.port }
        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def logout(self):
        message = { 'username': self.user.username, 'op': 3, 'ip': self.user.ip, 'port': self.user.port }
        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def parse_msg(self, data) -> Tuple[int, Response]:
        message = json.loads(data)
        return (1, Response(message["message"]))
    
    def receive_msg(self, address: Address):
        data = self.socket.recv(1024).decode("utf-8")

        if data: 
            ok, message = self.parse_msg(data)
            Logger.debug(f"Message received from {address}: {message.message}")

    def send_msg(self, request: str, address: Address):
        self.socket.send(request.encode("utf-8"))
        Logger.debug(f"Message sent to {address}: {request}")

username = input("Insert an username: ")
port = int(input("Insert the desired port: "))

client = Client("127.0.0.1", port, username, Address("127.0.0.1", "8080"))
client.connect(client.server_address)

while True:
    Logger.debug("1 - Find user | 2 - Signin | 3 - Logout")
    op = int(input())

    if(op == 1):
        username = input("Insert user's username: ")
        ip = input("Insert user's ip: ")
        client.find_user(User(username, ip, "0"))
    elif(op == 2):
        client.signin()
    elif(op == 3):
        client.logout()
    else:
        pass