class Response:
    def __init__(self, message: str):
        self.message = message

class Request:
    def __init__(self, op, ip, port, username, video_port, audio_port):
        self.op = op
        self.ip = ip
        self.port = port
        self.username = username
        self.video_port = video_port
        self.audio_port = audio_port

#nome , número da operação desejada,IP  e porta
    def __str__(self):
        return "{ " + f"username: {self.username}, op: {self.op}, ip: {self.ip}, port: {self.port}, video_port: {self.video_port}, audio_port: {self.audio_port}" + " }"