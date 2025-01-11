from model.User import User


class DBAdapter:
    def __init__(self):
        self.users_auth = {"1": 1, "2": 2}
        self.users = {1: User("andr", "Andrey"), 2: User("kalanod", "kalan")}

    def check_auth(self, username, password):
        if username in self.users_auth:
            return self.users_auth[username]
        return None

    def getUser(self, id):
        if id in self.users:
            return self.users[id]
        return None