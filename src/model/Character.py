class Character:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.picture = "new_character.png"
        self.sprites = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "sprites": self.sprites
        }
