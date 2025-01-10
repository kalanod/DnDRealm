class Character:
    def __init__(self, id, name, is_background):
        self.id = id
        self.name = name
        self.picture = "static/sprites/new_character.png"
        self.sprites = dict()
        self.is_background = is_background

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "sprites": self.sprites,
            "is_background": self.is_background
        }
