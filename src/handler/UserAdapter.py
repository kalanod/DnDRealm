
from handler.DBAdapter import DBAdapter
from handler.RoomAdapter import RoomAdapter
from model.User import User


class UserAdapter:
    def __init__(self):
        self.dbAdapter = DBAdapter()
        self.roomAdapter = RoomAdapter()

    def get_user(self, id) -> User:
        return self.dbAdapter.getUser(id)

    def joinRoom(self, code, user_id):
        room_id = self.roomAdapter.get_roomId_by_code(code)
        self.roomAdapter.addUser(room_id, user_id)
        if not room_id:
            return None
        return room_id
