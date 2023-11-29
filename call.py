import socket
import pyaudio

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
        self.audio_socket.bind((user.ip, user.audio_port))
    
    def receive_audio(self):
        output_stream = self.audio.open(format=pyaudio.paInt16, channels=self.CHANNELS, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)

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

        while True:
            try:
                message = input_stream.read(1024)
                # print(f"Sending message to: {dest.audio_port}")
                self.audio_socket.sendto(message, (dest.ip, dest.audio_port))
            except KeyboardInterrupt:
                input_stream.close()
                break