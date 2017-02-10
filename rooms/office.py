from rooms import Rooms

class Office(Rooms):
    """docstring for Office."""
    def __init__(self, arg):
        super(Office, Rooms).__init__()
        self.arg = arg
        self.totalSpace = 6
        self.allocatedStaffs = []
    def add_staff(self, staff):
        if staff != null:
            if staffExist():
                return "Staff is already allocated to this room"
            elif staffExistElsewhere():
                return "Staff is already allocated to another room"
            else:
                self.allocatedstaffs.append(staff)
                return True
    def remove_staff(self,staff):
        if staff != null:
            removed = False
            for i in range(0,len(self.allocatedstaffs)):
                if allocatedstaffs[i].ID == staff.ID:
                    #allocatedstaffs.splice(i,i+1)
                    removed = True
            if removed:
                return removed
            else:
                return "Staff is not allocated to this room"

    def checkAvailableSpace(self):
        return self.totalSpace - len(self.allocatedStaffs)
