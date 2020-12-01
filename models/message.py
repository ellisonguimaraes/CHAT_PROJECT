
class Message:
    def __init__(self, id, msg, date, id_user, is_recv, is_group=0):
        self.id = id
        self.msg = msg
        self.date = date
        self.id_user = id_user
        # 1: Is recv, 0: Is send
        self.is_recv = is_recv
        # 1: Is Group, 0: Is Private
        self.is_group = is_group

    def __str__(self):
        return f"({self.id}), DE: {self.id_user}, {self.date}: {self.msg}"
