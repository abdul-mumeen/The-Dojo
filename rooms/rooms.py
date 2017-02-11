class Rooms(object):
    def __init__(self, name):
        self.name = name
        self.allocated_fellows = []
        self.total_space = 4

    def add_fellow(self, fellow):
        if fellow != null:
            self.allocated_fellows.append(fellow)
            return True

    def isFull(self):
        if len(self.allocated_fellows) >= self.total_space:
            return True
        else:
            return False

    def remove_fellow(self, fellow):
        if fellow != null:
            removed = False
            for i in range(0, len(self.allocated_fellows)):
                if allocated_fellows[i].ID == fellow.ID:
                    #allocated_fellows.splice(i,i+1)
                    removed = True
            if removed:
                return removed
            else:
                return "Fellow is not allocated to this room"

    def checkAvailableSpace(self):
        return self.total_space - len(self.allocated_fellows)
