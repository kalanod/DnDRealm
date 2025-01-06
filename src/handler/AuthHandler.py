from src.model import AuthData, RegData


def auth(auth_data: AuthData):
    if auth_data.username == "1@1.1" and auth_data.password == "1":
        return True
    return False

def register(reg_data: RegData):
    return True