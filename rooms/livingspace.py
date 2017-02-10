from rooms import Rooms

class LivingSpace(Rooms):
    """docstring for LivingSpace."""
    def __init__(self, arg):
        super(LivingSpace, Rooms).__init__()
        self.arg = arg
