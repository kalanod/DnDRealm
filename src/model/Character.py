class Character:
    def __init__(self, id, name, is_background, picture="static/sprites/new_character.png", sprites=None):
        if sprites is None:
            sprites = dict()
        self.id = id
        self.name = name
        self.picture = picture
        self.sprites = sprites
        self.is_background = is_background

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "sprites": self.sprites,
            "is_background": self.is_background
        }
