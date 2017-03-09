from rooms.room import Room


class LivingSpace(Room):
    """This livingspace class inherits from the room class"""

    def __init__(self, name, total_space=4):
        super().__init__(name)
        self.total_space = total_space
