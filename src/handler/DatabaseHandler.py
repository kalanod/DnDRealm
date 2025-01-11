import json
import sqlite3

from src.model.Character import Character
from src.model.Room import Room


class DatabaseHandler:
    def __init__(self, db_path="example.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        """Создает таблицы в базе данных."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id TEXT PRIMARY KEY,
                name TEXT,
                master_id INTEGER,
                current_background TEXT,
                current_sprites TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY,
                room_id INTEGER,
                name TEXT,
                is_background BOOLEAN,
                picture TEXT,
                sprites TEXT,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sprites (
                id TEXT PRIMARY KEY,
                character_id INTEGER,
                sprite_url TEXT,
                height INTEGER,
                FOREIGN KEY(character_id) REFERENCES characters(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                room_id INTEGER,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
        """)

        self.connection.commit()

    def save_room(self, room: Room):
        print(room.current_background, str(room.current_sprites))
        self.cursor.execute(
            "REPLACE INTO rooms (id, name, master_id, current_background, current_sprites) VALUES (?, ?, ?, ?, ?)",
            (room.room_id, room.name, room.master_id, str(room.current_background), str(room.current_sprites)))
        self.connection.commit()

    def get_room(self, room_id):
        self.cursor.execute("SELECT id, name, master_id, current_background, current_sprites FROM rooms WHERE id = ?",
                            (room_id,))
        row = self.cursor.fetchone()
        if row:
            room = Room(name=row[1], room_id=row[0], master_id=row[2], current_background=row[3],
                        current_sprites=row[4])
            room.users = self.get_users_in_room(room_id)
            room.characters = self.get_characters(room_id)
            room.current_sprites = self.get_current_sprites(room_id)
            room.current_background = self.get_current_background(room_id)
            for character_id in room.characters:
                room.characters[character_id].sprites = self.get_sprites(character_id)
            return room
        return None


    def save_character(self, room_id, character: Character, d=1):
        self.cursor.execute(
            "REPLACE INTO characters (id, name, room_id, is_background, picture) VALUES (?, ?, ?, ?, ?)",
            (character.id, character.name, room_id, character.is_background, character.picture))
        if d:
            for sprite in character.sprites:
                self.save_sprite(character.id, sprite)
        self.connection.commit()

    def get_characters(self, room_id):
        self.cursor.execute("SELECT id, name, is_background, picture FROM characters WHERE room_id = ?",
                            (room_id,))
        rows = self.cursor.fetchall()
        characters = {}
        for row in rows:
            characters[row[0]] = Character(id=row[0], name=row[1], is_background=row[2], picture=row[3])
            characters[row[0]].sprites = self.get_sprites(row[0])
        return characters

    def save_sprite(self, character_id, sprite):
        print("__________________")
        print(sprite)
        self.cursor.execute(
            "REPLACE INTO sprites (id, character_id, sprite_url, height) VALUES (?, ?, ?, ?)",
            (sprite["sprite_id"], sprite["character_id"], sprite["sprite_url"], sprite["height"]))
        self.connection.commit()

    def get_sprites(self, character_id):
        self.cursor.execute("SELECT id, sprite_url, height FROM sprites WHERE character_id = ?", (character_id,))
        rows = self.cursor.fetchall()
        return {row[0]: {"sprite_url": row[1], "height": row[2], "character_id": character_id, "sprite_id": row[0]} for
                row in rows}

    def add_user_to_room(self, room_id, user_id):
        self.cursor.execute("INSERT INTO users (id, room_id) VALUES (?, ?)", (user_id, room_id))
        self.connection.commit()

    def get_users_in_room(self, room_id):
        self.cursor.execute("SELECT id FROM users WHERE room_id = ?", (room_id,))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_current_background(self, room_id):
        self.cursor.execute("SELECT current_background FROM rooms WHERE id = ?", (room_id,))
        d = str(self.cursor.fetchone()[0]).replace("'", '"')
        row = json.loads(d)
        return row

    def get_current_sprites(self, room_id):
        self.cursor.execute("SELECT current_sprites FROM rooms WHERE id = ?", (room_id,))
        d = str(self.cursor.fetchone()[0]).replace("'", '"')
        row = json.loads(d)
        return row

    def delete_character(self, character_id):
        """Удаляет персонажа из базы данных."""
        self.cursor.execute("DELETE FROM characters WHERE id = ?", (character_id,))
        self.cursor.execute("DELETE FROM sprites WHERE character_id = ?", (character_id,))
        self.connection.commit()

    def delete_room(self, room_id):
        """Удаляет комнату и связанные с ней данные."""
        self.cursor.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
        self.cursor.execute("DELETE FROM characters WHERE room_id = ?", (room_id,))
        self.cursor.execute("DELETE FROM users WHERE room_id = ?", (room_id,))
        self.connection.commit()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()

# Пример использования
# db_handler = DatabaseHandler("example.db")
# db_handler.save_room(Room("Example Room", 1, 123, "background.png"))
# room = db_handler.get_room(1)
# print(room.name, room.master_id)
