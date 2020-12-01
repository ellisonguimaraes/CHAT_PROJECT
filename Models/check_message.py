class CheckMessage:
    def __init__(self, id, id_user, id_message, is_check):
        self.id = id
        self.id_user = id_user
        self.id_message = id_message
        self.is_check = is_check

    def __str__(self):
        return f"User: {self.id_user}, Message: {self.id_message}, Check: {self.is_check}"
