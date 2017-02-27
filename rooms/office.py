from rooms.rooms import Room


class Office(Room):
    """This office class inherits from the room class"""

    def __init__(self, name, total_space=6):
        super().__init__(name)
        self.total_space = total_space
