import socket
import threading
import json
from call import AudioInterface
import cv2
#import rtp
import struct
import time
import pyaudio

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
        self.user = User(username, ip, port, video_port, audio_port)
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audioInterface = AudioInterface()
        self.socket.settimeout(90)
    
    def connect(self, address: Address):
        try:
            self.socket.connect((address.ip, int(address.port)))
            Logger.debug(f"Successful connection to: {address}")
        except socket.error as e:
            Logger.debug(f"Unsuccessful connection to: {address}")
            Logger.debug(e)

    def find_user(self, user: User):
        message = { 'username': user.username, 'op': 1, 'ip': user.ip, 'port': '' , 'video_port': '', 'audio_port': '', 'destination_ip': '', 'destination_port': '' }
        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def signin(self):
        message = { 'username': self.user.username, 'op': 2, 'ip': self.user.ip, 'port': self.user.port, 'video_port': self.user.video_port, 'audio_port': self.user.audio_port, 'destination_ip': '', 'destination_port': '' }
        self.send_msg(json.dumps(message), self.server_address)
        self.receive_msg(self.server_address)

    def logout(self):
        message = { 'username': self.user.username, 'op': 3, 'ip': self.user.ip, 'port': self.user.port, 'video_port': self.user.video_port, 'audio_port': self.user.audio_port, 'destination_ip': '', 'destination_port': '' }
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
            if(message.message == "Call accepted"):
                #threads do video_call e audio_call
                print("Começou a chamada")
            if(message.message.startswith("Calling")):
                print("Do you accept the call?")
                answer = int(input("1 for yes ou 0 for not: "))
                caller = message.message.split(",")
                if(answer > 0):
                    message2 = { 'username': caller[1], 'op': 5, 'ip': caller[3], 'port': caller[4], 'video_port': caller[5], 'audio_port': caller[6], 'destination_ip': self.user.ip, 'destination_port': self.user.port }
                    self.send_msg(json.dumps(message2), self.server_address)
                    #threads do video_call e audio_call
                    print("Começou a chamada")
                else:
                    message2 = { 'username': caller[1], 'op': 6, 'ip': caller[3], 'port': caller[4], 'video_port': caller[5], 'audio_port': caller[6], 'destination_ip': self.user.ip, 'destination_port': self.user.port }
                    self.send_msg(json.dumps(message2), self.server_address)

    def send_msg(self, request: str, address: Address):
        self.socket.send(request.encode("utf-8"))
        # Logger.debug(f"Message sent to {address}: {request}")
        
    def make_a_call(self, address: Address,):
        message = { 'username': self.user.username, 'op': 4, 'ip': self.user.ip, 'port': self.user.port, 'video_port': self.user.video_port, 'audio_port': self.user.audio_port, 'destination_ip': address.ip, 'destination_port': address.port }
        self.send_msg(json.dumps(message), self.server_address)
    
    def audio_call(self, user: User):
        threading.Thread(target=self.audioInterface.receive_audio).start()
        threading.Thread(target=self.audioInterface.send_audio, args=(user,)).start()
    
    def video_call(self,dest_IP,dest_port):
        sNumber = 0
        # Initialize video capture using OpenCV
        cap = cv2.VideoCapture(0)  # Use 0 for the default webcam, change if necessary

        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("If you want to close the connection type \"q\" on the window")
            while True:
                # Capture frame-by-frame
                ret, frame = cap.read()

                # Display the frame
                cv2.imshow('Video Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Encode frame to JPEG
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                _, encoded_frame = cv2.imencode('.jpg', frame, encode_param)

                # Create RTP packet
                rtp_packet = pack_rtp_packet(encoded_frame.tobytes(),sNumber,int(time.time()),self.user.video_port)
                sNumber += 1
                # Get the packet bytes
                packet_bytes = rtp_packet

                # Send the packet over UDP
                udp_socket.sendto(packet_bytes, (dest_IP, int(dest_port)))
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            # Release the video capture, close UDP socket, and destroy OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
            udp_socket.close()

username = input("Insert an username: ")
port = int(input("Insert the desired port: "))
video_port = int(input("Insert the desired port for video: "))
audio_port = int(input("Insert the desired port for audio: "))

client = Client("127.0.0.1", port, video_port, audio_port, username, Address("127.0.0.1", "8080"))
client.connect(client.server_address)

def pack_rtp_packet(data, sequence_number, timestamp, ssrc):
    version = 2
    padding = 0
    extension = 0
    cc = 0
    marker = 0
    PAYLOAD_TYPE = 96

    # RTP header
    rtp_header = struct.pack(
        "!BBHII",
        (version << 6) | (padding << 5) | (extension << 4) | cc,
        (marker << 7) | PAYLOAD_TYPE,
        sequence_number,
        timestamp,
        ssrc,
    )

    # RTP packet (header + data)
    rtp_packet = rtp_header + data

    return rtp_packet


while True:
    Logger.debug("1 - Find user | 2 - Signin | 3 - Logout | 4 - Make a Call")
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
        dest_IP = input("Insert the IP of who you want to call: ")
        dest_port = input("Insert the Port of who you want to call: ")
        #ask if patner wants to connect
        client.make_a_call(Address(dest_IP, dest_port))
    else:
        pass