class Rooms(object):
    def __init__(self,name):
        self.name = name
        self.allocatedFellows = []
        self.totalSpace = 4
    def add_fellow(self, fellow):
        if fellow != null:
            if fellowExist():
                return "Fellow is already allocated to this room"
            elif fellowExistElsewhere():
                return "Fellow is already allocated to another room"
            else:
                self.allocatedFellows.append(fellow)
                return True
    def remove_fellow(self,fellow):
        if fellow != null:
            removed = False
            for i in range(0,len(self.allocatedFellows)):
                if allocatedFellows[i].ID == fellow.ID:
                    #allocatedFellows.splice(i,i+1)
                    removed = True
            if removed:
                return removed
            else:
                return "Fellow is not allocated to this room"

    def checkAvailableSpace(self):
        return self.totalSpace - len(self.allocatedFellows)
