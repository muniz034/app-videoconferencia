class User:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port

    def __str__(self):
        return "{ " + f"username: {self.username}, ip: {self.ip}, port: {self.port}" + " }"