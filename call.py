import pyaudio

class AudioInterface:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 8000
    CHUNK = 1024
    PAYLOAD_TYPE = 11

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(format=pyaudio.paInt16, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.output_stream = self.audio.open(format=pyaudio.paInt16, channels=self.CHANNELS, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)

    def write(self, data):
        self.output_stream.write(data)
    
    def read(self):
        return self.input_stream.read(1024)