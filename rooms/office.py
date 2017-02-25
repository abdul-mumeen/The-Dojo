from rooms.rooms import Rooms

class Office(Rooms):
    """This office class inherits from the room class"""
    def __init__(self, name):
        super().__init__(name)
        self.total_space = 6
