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
        print(data)
        new_character = 0
        if "new_sprite" in data:
            if data["new_sprite"]["character_id"] not in self.rooms[room_id].current_sprites:
                new_character = 1
            self.rooms[room_id].current_sprites[data["new_sprite"]["character_id"]] = \
                {'sprite_url': data["new_sprite"]["sprite_url"],
                 "height": 400,
                 "character_id": data["new_sprite"]["character_id"],
                 "sprite_id": data["new_sprite"]["sprite_id"]}
            return {'current_sprites': self.rooms[room_id].current_sprites, "new_character": new_character}
        if "current_background" in data:
            self.rooms[room_id].current_background = data["current_background"]
            return {'current_background': self.rooms[room_id].current_background}

    def addUser(self, room_id, user_id):
        self.rooms[room_id].users.append(user_id)

    def get_current(self, room_id):
        return {'current_sprites': self.rooms[room_id].current_sprites}

    def addCharacter(self, room_id):
        c_id = random.randint(0, 99999)
        while c_id in self.rooms[room_id].characters:
            c_id = random.randint(0, 99999)
        self.rooms[room_id].characters[str(c_id)] = Character(c_id, "New")

    def delete_character(self, room_id, character_id):
        self.rooms[room_id].characters.pop(character_id)

    def get_characters(self, room_id):
        characters = self.get_room(room_id).characters
        return {character_id: characters[character_id].to_dict() for character_id in characters}

    def updateCharacter(self, room_id, character_id, character_name):
        self.get_room(room_id).characters[character_id].name = character_name

    def addSprite(self, room_id, character_id, file_url):
        if len(self.get_room(room_id).characters[character_id].sprites) == 0:
            self.get_room(room_id).characters[character_id].picture = file_url
        sprite_id = random.randint(0, 99999)
        while sprite_id in self.get_room(room_id).characters[character_id].sprites:
            sprite_id = random.randint(0, 99999)
        sprite = {"sprite_url": file_url, "height": 400, "character_id": character_id, "sprite_id": str(room_id) + "|" + str(sprite_id)}
        self.get_room(room_id).characters[character_id].sprites[str(room_id) + "|" + str(sprite_id)] = sprite
        return sprite

    def delete_sprite(self, room_id, data):
        print("data", data)
        print("syb", self.get_room(room_id).characters[data["character_id"]].sprites)
        print(self.get_room(room_id).current_sprites)
        self.get_room(room_id).characters[data["character_id"]].sprites.pop(data["sprite_id"])
        if data["character_id"] in self.get_room(room_id).current_sprites:
            self.get_room(room_id).current_sprites.pop(data["character_id"])
        if len(self.get_room(room_id).characters[data["character_id"]].sprites) == 0:
            self.get_room(room_id).characters[data["character_id"]].picture = "static/sprites/new_character.png"

    def remove_current(self, room_id, data):
        self.get_room(room_id).current_sprites.pop(data["character_id"])
