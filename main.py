from call import AudioInterface

audioInterface = AudioInterface()

try:
    while True:
        data = audioInterface.read()
        audioInterface.write(data)
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audioInterface.in_stream.stop_stream()
    audioInterface.out_stream.stop_stream()
    audioInterface.in_stream.close()
    audioInterface.out_stream.close()
    audioInterface.audio.terminate()