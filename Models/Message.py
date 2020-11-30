
class Message:
    def __init__(self, id, msg, date, id_user, recv):
        self.id = id
        self.msg = msg
        self.date = date
        self.id_user = id_user
        # If 1 == Recv, 0 = Send
        self.recv = recv

    def __str__(self):
        return f"({self.id}), DE: {self.id_user}, {self.date}: {self.msg}"
