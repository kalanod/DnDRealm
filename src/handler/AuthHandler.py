from handler.DBAdapter import DBAdapter
from model import AuthData, RegData


class AuthHandler:
    def __init__(self, session):
        self.session = session
        self.dbAdapter = DBAdapter()
    def auth(self, auth_data: AuthData):
        user_id = self.dbAdapter.check_auth(auth_data.username, auth_data.password)
        if user_id:
            self.session['user_id'] = user_id
            return True
        return False

    def register(self, reg_data: RegData):
        return True
