
class Message:
    def __init__(self, id, msg, date, id_user):
        self.id = id
        self.msg = msg
        self.date = date
        self.id_user = id_user

    def __str__(self):
        return f"({self.id}), DE: {self.id_user}, {self.date}: {self.msg}"
