from src.model.Room import Room


class RoomAdapter:
    def __init__(self):
        self.rooms = {1: Room("name", 1, 1)}

    def get_room(self, room_id) -> Room:
        return self.rooms[room_id]

    def get_roomId_by_code(self, room_code):
        return 1

    def updateRoom(self, room_id, data):
        if "new_sprite" in data:
            self.rooms[room_id].current_sprites.append({'url': data["new_sprite"], "height": 200})
            return {'current_sprites': self.rooms[room_id].current_sprites}
        if "current_background" in data:
            self.rooms[room_id].current_background = data["current_background"]
            return {'current_background': self.rooms[room_id].current_background}

    def addUser(self, room_id, user_id):
        self.rooms[room_id].users.append(user_id)

    def get_current(self, room_id):
        return
