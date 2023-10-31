from typing import List, Tuple, Union
import socket
import threading
from enum import Enum
import json
from typing import Dict

from logger import Logger
from user import User
from message import Response, Request

class Operation(Enum):
    FIND_USER = 1
    INSERT_USER = 2
    REMOVE_USER = 3

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"{self.ip}:{self.port}"

class Controller:
    def __init__(self):
        self.users: List[User] = []

    def find_user(self, username, ip) -> Tuple[int, User]:
        # Logger.debug(f"Call to method find_user: username({username}) ip({ip})")
        index = -1
        for i, user in enumerate(self.users):
            if user.username == username and user.ip == ip:
                index = i
                break
        if index > -1:
            return (index, user)
        else:
            return (-1, None)
        
    def insert_user(self, username, ip, port):
        # Logger.debug(f"Call to method insert_user: username({username}) ip({ip}) port({port})")
        user_existe = self.user_exists(username, ip)
        if not user_existe:
            self.users.append(User(username, ip, port))
            return 1
        else:
            return -1
        
    def remove_user(self, username, ip):
        # Logger.debug(f"Call to method remove_user: username({username}) ip({ip})")
        user_index, _ = self.find_user(username, ip)
        if user_index > -1:
            self.users.pop(user_index)
            return 1
        else:
            return -1

    def user_exists(self, username, ip):
        # Logger.debug(f"Call to method user_exists: username({username}) address({address})")
        return any(user.username == username and user.ip == ip for user in self.users)
    
    def print_table(self):
        if(len(self.users) == 0): return
        
        data = [["IP", "Username", "Port"]]

        for i in range(len(self.users)):
            data.append([self.users[i].ip, self.users[i].username, self.users[i].port])

        columns_widths = [max(len(str(item)) for item in column) for column in zip(*data)]

        Logger.debug("IP TABLE")
        for row in data:
            print("  ".join(f"{item:{width}}" for item, width in zip(row, columns_widths)))

class Server:
    def __init__(self, ip, port, n_clientes):
        self.controller = Controller()
        self.ip = ip
        self.port = port
        self.n_clientes = n_clientes
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(90)
        self.client_table: Dict[str, socket.socket] = {}
    
    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        Logger.debug(f"Server started at {self.ip}:{self.port}")
    
    def accept(self):
        client_socket, client_address = self.socket.accept()
        client_socket.settimeout(180)
        Logger.debug(f"Connection accepted from {client_address[0]}:{client_address[1]}")
        self.client_table[f"{client_address[0]}:{client_address[1]}"] = client_socket
        return client_socket, client_address
    
    def process_msg(self, message: Request) -> Tuple[int, str]:
        if(message.op is Operation.FIND_USER):
            index, result = self.controller.find_user(message.username, message.ip)
            return Response(json.dumps({ 'message': str(result) })) if index > -1 else Response(json.dumps({ 'message': "User not found" }))

        if(message.op is Operation.INSERT_USER):
            result = self.controller.insert_user(message.username, message.ip, message.port)
            return Response(json.dumps({ 'message': "User created" })) if result == 1 else Response(json.dumps({ 'message': "User already exists" }))

        if(message.op is Operation.REMOVE_USER):
            result = self.controller.remove_user(message.username, message.ip)
            return Response(json.dumps({ 'message': "User removed" })) if result == 1 else Response(json.dumps({ 'message': "User don't exists" }))

    def parse_msg(self, data) -> Tuple[int, Request]:
        message = json.loads(data)
        op = -1

        try:
            op = Operation(int(message["op"]))
        except ValueError as e:
            return (-1, "Op code not found")
        
        return (1, Request(op, message["ip"], message["port"], message["username"]))
    
    def receive_msg(self, address: Address):
        client_socket = self.client_table.get(str(address))
        data = client_socket.recv(1024).decode("utf-8")

        if data: 
            ok, message = self.parse_msg(data)
            if(not ok): return self.send_msg(message, address)
            # Logger.debug(f"Message received from {address}: {message}")
            
            return self.send_msg(self.process_msg(message), address)

    def send_msg(self, response: Response, address: Address):
        client_socket = self.client_table.get(str(address))
        client_socket.send(response.message.encode("utf-8"))
        self.controller.print_table()
        # Logger.debug(f"Message sent to {address}: {response.message}")

    def end(self, address: Address):
        client_socket = self.client_table.get(str(address))
        client_socket.close()


def client_listener(server: Server, address: Address):
    while True:
        try:
            server.receive_msg(address)
        except socket.timeout:
            Logger.debug("Closing...")
            break
        
if __name__ == "__main__":
    server = Server("127.0.0.1", 8080, 1)
    server.start()

    while True:
        try:
            connection, address = server.accept()
            threading.Thread(target=client_listener, args=(server, Address(address[0], address[1]))).start()
        except socket.timeout:
            Logger.debug("Closing...")
            break