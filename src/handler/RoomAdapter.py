import random
from random import Random

from src.model.Character import Character
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
            self.rooms[room_id].current_sprites.append({'url': data["new_sprite"], "height": 400})
            return {'current_sprites': self.rooms[room_id].current_sprites}
        if "current_background" in data:
            self.rooms[room_id].current_background = data["current_background"]
            return {'current_background': self.rooms[room_id].current_background}

    def addUser(self, room_id, user_id):
        self.rooms[room_id].users.append(user_id)

    def get_current(self, room_id):
        return

    def addCharacter(self, room_id):
        c_id = random.randint(0, 99999)
        while c_id in self.rooms[room_id].characters:
            c_id = random.randint(0, 99999)
        self.rooms[room_id].characters[c_id]= Character(c_id, "New")

    def delete_character(self, room_id, character_id):
        self.rooms[room_id].characters.pop(character_id)

    def get_characters(self, room_id):
        characters = self.get_room(room_id).characters
        return [characters[character_id].to_dict() for character_id in characters]

    def updateCharacter(self, room_id, character_id, character_name):
        self.get_room(room_id).characters[character_id].name = character_name

    def addSprite(self, room_id, character_id, file_url):
        return self.get_room(room_id).characters[int(character_id)].sprites.append(file_url)
