class User:
    def __init__(self, username, ip, server_port, port, video_port, audio_port):
        self.username = username
        self.ip = ip
        self.port = port
        self.video_port = video_port
        self.audio_port = audio_port
        self.server_port = server_port

    def __str__(self):
        return "{ " + f"username: {self.username}, ip: {self.ip}, server_port: {self.server_port}, port: {self.port}, video_port: {self.video_port}, audio_port: {self.audio_port}" + " }"