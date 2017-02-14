from rooms.rooms import Rooms

class Office(Rooms):
    """This office class inherits from the room class"""
    def __init__(self, name):
        super().__init__(name)
        self.totalSpace = 6
        self.allocatedStaffs = []

    def add_fellow(self, staff):
        if staff != null:
            self.allocatedStaffs.append(staff)
            return True

    def isFull(self):
        if len(self.allocated_fellows) + len(self.allocatedStaffs) >= self.totalSpace:
            return True
        else:
            return False

    def remove_fellow(self, staff):
        if staff != null:
            removed = False
            for i in range(0, len(self.allocatedStaffs)):
                if allocatedStaffs[i].ID == staff.ID:
                    #allocatedFellows.splice(i,i+1)
                    removed = True
            if removed:
                return removed
            else:
                return "Staff is not allocated to this room"

    def checkAvailableSpace(self):
        return self.totalSpace - (len(self.allocatedStaffs) + len(self.allocated_fellows))
