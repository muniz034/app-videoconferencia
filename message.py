class Response:
    def __init__(self, message: str):
        self.message = message

class Request:
    def __init__(self, op, username, video_port, audio_port, dest_username, dest_ip):
        self.op = op
        self.username = username
        self.video_port = video_port
        self.audio_port = audio_port
        self.dest_username = dest_username
        self.dest_ip = dest_ip