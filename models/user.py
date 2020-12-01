class User:
    def __init__(self, id, name, ip, port, status):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.status = status

    def __str__(self):
        return f"{self.id} ~ {self.name}, {self.ip}:{self.port}\t{self.status}"
