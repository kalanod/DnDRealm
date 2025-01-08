class Room:

    def __init__(self, name, room_id, master_id, current_background=None, current_sprites=None, users=None):
        if users is None:
            users = []
        if current_sprites is None:
            current_sprites = []
        self.room_id = room_id
        self.master_id = master_id
        self.name = name
        self.users = []
        self.current_background = current_background
        self.current_sprites = current_sprites

    def to_dict(self):
        return {
            "name": self.name,
            "room_id": self.room_id,
            "master_id": self.master_id,
            "current_background": self.current_background,
            "current_sprites": self.current_sprites,
            "users": self.users
        }
