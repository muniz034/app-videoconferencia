import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

class AudioInterface:
    def __init__(self):
        audio = pyaudio.PyAudio()
        self.input_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.output_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

    def write(self, data):
        self.output_stream.write(data)
    
    def read(self):
        return self.input_stream.read(1024)