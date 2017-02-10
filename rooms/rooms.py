class Rooms(object):
    def __init__(self, name):
        self.name = name
        self.allocatedFellows = []
        self.totalSpace = 4

    def add_fellow(self, fellow):
        if fellow != null:
            self.allocatedFellows.append(fellow)
            return True

    def isFull(self):
        if len(self.allocatedFellows) >= self.totalSpace:
            return True
        else:
            return False
                                
    def remove_fellow(self, fellow):
        if fellow != null:
            removed = False
            for i in range(0, len(self.allocatedFellows)):
                if allocatedFellows[i].ID == fellow.ID:
                    #allocatedFellows.splice(i,i+1)
                    removed = True
            if removed:
                return removed
            else:
                return "Fellow is not allocated to this room"

    def checkAvailableSpace(self):
        return self.totalSpace - len(self.allocatedFellows)
