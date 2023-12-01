import socket
from time import sleep
import pyaudio
import vidstream

from user import User

class AudioInterface:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    def __init__(self):
        self.audio = pyaudio.PyAudio()
    
    def start_socket(self, user: User):
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_socket.bind((user.ip, int(user.audio_port)))
    
    def receive_audio(self):
        output_stream = self.audio.open(format=pyaudio.paInt16, channels=self.CHANNELS, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)
        self.output_stream = output_stream

        while True:
            try:
                data, server = self.audio_socket.recvfrom(2048)
                # print(f"Receiving message from: {server}")
                output_stream.write(data)
            except KeyboardInterrupt:
                output_stream.close()
                break

    def send_audio(self, dest: User):
        input_stream = self.audio.open(format=pyaudio.paInt16, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.input_stream = input_stream

        while True:
            try:
                message = input_stream.read(1024)
                # print(f"Sending message to: {dest.audio_port}")
                self.audio_socket.sendto(message, (dest.ip, int(dest.audio_port)))
            except KeyboardInterrupt:
                input_stream.close()
                break

    def stop_stream(self):
        self.input_stream.close()
        self.output_stream.close()

class VideoInterface:
    def start_streaming_server(self, user: User):
        server = vidstream.StreamingServer(user.ip, int(user.video_port))
        server.start_server()
        while True:
            pass

    def start_camera(self, dest: User):
        client = vidstream.CameraClient(dest.ip, int(dest.video_port))
        client.start_stream()
        while True:
            pass