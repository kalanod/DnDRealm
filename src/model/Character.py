class Character:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.picture = "static/sprites/new_character.png"
        self.sprites = dict()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "sprites": self.sprites
        }
