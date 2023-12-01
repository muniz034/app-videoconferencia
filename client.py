import socket
import threading
import json
import call
import cv2
import struct
import time
import pyaudio
import pickle
import vidstream

from typing import Tuple

from logger import Logger
from message import Request, Response
from user import User

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"{self.ip}:{self.port}"

class Client:
    def __init__(self, ip, port, video_port, audio_port, username, server_address: Address):
        self.user = User(username, ip, 0, video_port, audio_port)
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audioInterface = call.AudioInterface()
        self.videoInterface = call.VideoInterface()
        self.socket.settimeout(900)
    
    def connect(self, address: Address):
        try:
            self.socket.connect((address.ip, int(address.port)))
            Logger.debug(f"Successful connection to: {address}")
        except socket.error as e:
            Logger.debug(f"Unsuccessful connection to: {address}")
            Logger.debug(e)

    def find_user(self, user: User):
        message = { 
            'username': user.username, 
            'op': 1, 
            'video_port': '', 
            'audio_port': '', 
            'dest_username': '', 
            'dest_ip': user.ip 
        }

        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def signin(self):
        message = { 
            'username': self.user.username, 
            'op': 2, 
            'video_port': self.user.video_port, 
            'audio_port': self.user.audio_port, 
            'dest_username': '', 
            'dest_ip': '' 
        }

        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def logout(self):
        message = { 
            'username': self.user.username, 
            'op': 3, 
            'video_port': self.user.video_port, 
            'audio_port': self.user.audio_port, 
            'dest_username': '', 
            'dest_ip': '' 
        }

        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def send_call(self, dest_username, dest_ip):
        message = { 
            'username': self.user.username, 
            'op': 4, 
            'video_port': '', 
            'audio_port': '',
            'dest_username': dest_username, 
            'dest_ip': dest_ip 
        }

        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def start_call(self, caller: User):
        # Logger.debug(f"CALL STARTED WITH {caller.username}")
        self.audio_call(self.user, caller)
        self.video_call(self.user, caller)
        
    def start_call2(self, caller: User):
        # Logger.debug(f"CALL STARTED WITH {caller.username}")
        self.audio_call(self.user, caller)
        self.video_call2(self.user, caller)

    def receive_call(self, caller: User):
        Logger.debug(f"Call from {caller.username}. Do you accept the call?")
        answer = int(input("1 (YES) | 0 (NO): "))
        if(answer == 1):
            self.send_msg(json.dumps(
                { 
                    'username': self.user.username, 
                    'op': 5, 
                    'video_port': '', 
                    'audio_port': '',
                    'dest_username': caller.username, 
                    'dest_ip': caller.ip 
                }), 
                self.server_address
            )

            self.receive_msg(self.server_address)
            self.start_call2(caller)
        else:
            self.send_msg(json.dumps(
                {
                    'username': self.user.username,
                    'op': 6, 
                    'video_port': '', 
                    'audio_port': '',
                    'dest_username': caller.username, 
                    'dest_ip': caller.ip 
                }), 
                self.server_address
            )
            self.receive_msg(self.server_address)

    def parse_msg(self, data) -> Tuple[int, Response]:
        message = json.loads(data)
        return (1, Response(message["message"]))
    
    def receive_msg(self, address: Address):
        data = self.socket.recv(1024).decode("utf-8")

        if data: 
            ok, message = self.parse_msg(data)
            if(message.message == "Ringing"):
                self.receive_msg(self.server_address)
            elif(message.message.startswith("Call from")):
                info = message.message.split(",")
                caller = User(info[1], info[2], info[3], info[4], info[5])
                self.receive_call(caller)
            elif(message.message.startswith("Call accepted")):
                info = message.message.split(",")
                dest = User(info[1], info[2], info[3], info[4], info[5])
                self.start_call(dest)
            else:
                Logger.debug(f"Message received from {address}: {message.message}")

    def wait_for_msg(self):
        while True:
            self.receive_msg(self.server_address)

    def send_msg(self, request: str, address: Address):
        self.socket.send(request.encode("utf-8"))
        # Logger.debug(f"Message sent to {address}: {request}")
    
    def audio_call(self, user: User, dest: User):
        self.audioInterface.start_socket(user)
        threading.Thread(target=self.audioInterface.receive_audio).start()
        threading.Thread(target=self.audioInterface.send_audio, args=(dest,)).start()

    def video_call(self, user: User, dest: User):
        threading.Thread(target=self.videoInterface.start_camera, args=(user,)).start()
        threading.Thread(target=self.videoInterface.start_streaming_server, args=(dest,)).start()
        
    def video_call2(self, user: User, dest: User):
        threading.Thread(target=self.videoInterface.start_screen, args=(user,)).start()
        threading.Thread(target=self.videoInterface.start_streaming_server, args=(dest,)).start()

username = input("Insert an username: ")
video_port = int(input("Insert the desired port for video: "))
audio_port = int(input("Insert the desired port for audio: "))

client = Client("127.0.0.1", 0, video_port, audio_port, username, Address("127.0.0.1", "8080"))
client.connect(client.server_address)

while True:
    Logger.debug("1 - Find user | 2 - Signin | 3 - Logout | 4 - Make a Call | 7 - Listen")
    op = int(input("Insert a op code: "))

    if(op == 1):
        username = input("Insert user's username: ")
        ip = input("Insert user's ip: ")
        client.find_user(User(username, ip, "0", "0", "0"))
    elif(op == 2):
        client.signin()
    elif(op == 3):
        client.logout()
    elif(op == 4):
        dest_username = input("Insert the username of who you want to call: ")
        dest_ip = input("Insert the IP of who you want to call: ")
        client.send_call(dest_username, dest_ip)
    elif(op == 7):
        client.receive_msg(client.server_address)
    else:
        pass