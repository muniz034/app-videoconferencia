class Response:
    def __init__(self, message: str):
        self.message = message

class Request:
    def __init__(self, op, ip, server_port, port, username, video_port, audio_port, destination_ip, destination_port):
        self.op = op
        self.ip = ip
        self.port = port
        self.username = username
        self.video_port = video_port
        self.audio_port = audio_port
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.server_port = server_port

#nome , número da operação desejada, IP, porta TC/IP, porta para video, porta para audio
    def __str__(self):
        return "{ " + f"username: {self.username}, op: {self.op}, ip: {self.ip}, server_port: {self.server_port}, port: {self.port}, video_port: {self.video_port}, audio_port: {self.audio_port}, destination_ip: {self.destination_ip}, destination_port: {self.destination_port}" + " }"