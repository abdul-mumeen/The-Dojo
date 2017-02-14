from rooms.rooms import Rooms

class LivingSpace(Rooms):
    """This livingspace class inherits from the room class"""
    def __init__(self, name):
        super().__init__(name)
