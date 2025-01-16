import random
from random import Random

from handler.DatabaseHandler import DatabaseHandler
from model.Character import Character
from model.Room import Room


class RoomAdapter:
    def __init__(self, db_path="example.db"):
        self.db_path = db_path
        self.rooms = {}
        self.ensure_default_room()

    def ensure_default_room(self):
        db_handler = self.get_db_handler()
        room = db_handler.get_room(1)
        if not room:
            room = Room(name="Default Room", room_id=1, master_id="1", current_background=None)
            db_handler.save_room(room)
            self.rooms[1] = room

    def get_db_handler(self):
        return DatabaseHandler(self.db_path)

    def get_room(self, room_id) -> Room:
        if room_id not in self.rooms:
            db_handler = self.get_db_handler()
            room = db_handler.get_room(room_id)
            if room:
                room.characters = db_handler.get_characters(room_id)
                for char_id, char in room.characters.items():
                    char.sprites = db_handler.get_sprites(char_id)
                self.rooms[room_id] = room
        print(self.rooms.get(room_id))

        return self.rooms.get(room_id)

    def get_roomId_by_code(self, room_code):
        return 1  # Placeholder for actual implementation

    def updateRoom(self, room_id, data):
        room = self.get_room(room_id)
        new_character = 0
        db_handler = self.get_db_handler()
        print("update_room")
        print("data=", data)
        if "new_sprite" in data:
            character_id = data["new_sprite"]["character_id"]
            if character_id not in room.current_sprites:
                new_character = 1
            sprite = {
                'sprite_url': data["new_sprite"]["sprite_url"],
                "height": 600,
                "character_id": character_id,
                "sprite_id": data["new_sprite"]["sprite_id"]
            }
            room.current_sprites[character_id] = sprite
            db_handler.save_sprite(character_id, sprite)
            db_handler.save_room(room)
            return {'current_sprites': room.current_sprites, "new_character": new_character}
        if "current_background" in data:
            room.current_background = data["current_background"]
            db_handler.save_room(room)
            return {'current_background': room.current_background}

    def addUser(self, room_id, user_id):
        room = self.get_room(room_id)
        if user_id not in room.users:
            room.users.append(user_id)
            db_handler = self.get_db_handler()
            db_handler.add_user_to_room(room_id, user_id)

    def get_current(self, room_id):
        room = self.get_room(room_id)
        return {'current_sprites': room.current_sprites}

    def addCharacter(self, room_id):
        room = self.get_room(room_id)
        c_id = random.randint(0, 99999)
        while str(c_id) in room.characters:
            c_id = random.randint(0, 99999)
        character = Character(str(c_id), "New", False)
        room.characters[str(c_id)] = character
        db_handler = self.get_db_handler()
        db_handler.save_character(room_id, character)

    def addBackground(self, room_id):
        room = self.get_room(room_id)
        c_id = random.randint(0, 99999)
        while str(c_id) in room.characters:
            c_id = random.randint(0, 99999)
        character = Character(str(c_id), "New", True)
        room.characters[str(c_id)] = character
        db_handler = self.get_db_handler()
        db_handler.save_character(room_id, character)

    def delete_character(self, room_id, character_id):
        room = self.get_room(room_id)
        room.characters.pop(str(character_id), None)
        db_handler = self.get_db_handler()
        db_handler.delete_character(character_id)

    def get_characters(self, room_id):
        room = self.get_room(room_id)
        return {character_id: character.to_dict() for character_id, character in room.characters.items() if not character.is_background}

    def get_backgrounds(self, room_id):
        room = self.get_room(room_id)
        return {character_id: character.to_dict() for character_id, character in room.characters.items() if character.is_background}

    def updateCharacter(self, room_id, character_id, character_name):
        room = self.get_room(room_id)
        character = room.characters[character_id]
        character.name = character_name
        db_handler = self.get_db_handler()
        db_handler.save_character(room_id, character, 0)

    def addSprite(self, room_id, character_id, file_url):
        room = self.get_room(room_id)
        character = room.characters[character_id]
        if len(character.sprites) == 0:
            character.picture = file_url
        sprite_id = random.randint(0, 99999)
        while sprite_id in character.sprites:
            sprite_id = random.randint(0, 99999)
        sprite = {
            "sprite_url": file_url,
            "height": 600,
            "character_id": character_id,
            "sprite_id": str(room_id) + "|" + str(sprite_id)
        }
        character.sprites[sprite["sprite_id"]] = sprite
        if len(character.sprites) == 1:
            db_handler = self.get_db_handler()
            db_handler.save_character(room_id, character, d=0)
        db_handler = self.get_db_handler()
        print("new sprite")
        print(sprite)
        db_handler.save_sprite(character_id, sprite)
        return sprite

    def delete_sprite(self, room_id, data):
        room = self.get_room(room_id)
        character = room.characters[data["character_id"]]
        character.sprites.pop(data["sprite_id"], None)
        if data["character_id"] in room.current_sprites:
            room.current_sprites.pop(data["character_id"], None)
        if len(character.sprites) == 0:
            character.picture = "static/sprites/new_character.png"
            db_handler = self.get_db_handler()
            db_handler.save_character(room_id, character)
        db_handler = self.get_db_handler()
        db_handler.save_character(room_id, character)

    def remove_current(self, room_id, data):
        room = self.get_room(room_id)
        room.current_sprites.pop(data["character_id"], None)
        db_handler = self.get_db_handler()
        db_handler.save_room(room)
