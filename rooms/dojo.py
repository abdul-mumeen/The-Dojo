from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace

class Dojo(object):
    def __init__(self):
        self.all_rooms = []
        self.listOfStaffs = []
        self.listOfFellows = []

    def create_room(self, room_name, room_type):
        log = ""
        if room_type.strip() != "" and len(room_name) > 0:

            #can refactor to have createOffice and createLivingSpace
            if room_type == "office":
                for i in range(0, len(room_name)):
                    if room_name[i].strip() == "":
                        log += "\nThe office at index " + str(i) + " cannot be created due to empty name."
                    elif self.roomNameExist(room_name[i]):
                        log += "\nThe office at index " + str(i) + " already existed."
                    else:
                        new_room = Office(room_name[i])
                        self.all_rooms.append(new_room)
            elif room_type == "livingspace":
                for i in range(0, len(room_name)):
                    if room_name[i].strip() == "":
                        log += "\nThe livingspace at index " + str(i) + \
                        " cannot be created due to empty name."
                    elif self.roomNameExist(room_name[i]):
                        log += "\nThe name of livingspace " + str(i) + " already existed."
                    else:
                        new_room = LivingSpace(room_name[i])
                        self.all_rooms.append(new_room)
            else:
                log += "\nCannot create room(s), invalid room type enterred"
        else:
            log += "Cannot create rooms with empty room name and/or empty room type"

        if log == "":
            return True
        else:
            return log


    def add_person(self, name, designation, wants_accommodation="N"):
        if name.strip() != "":
            if designation.lower().strip() == "fellow":
                new_fellow = Fellow()
                new_fellow.name = name
                new_fellow.ID = self.getID("fellow")
                new_fellow.office = self.assignOffice(new_fellow.ID)
                if wants_accommodation.upper() == "Y":
                    new_fellow.livingspace = self.assignLivingspace(new_fellow.ID)

                self.listOfFellows.append(new_fellow)
                return new_fellow
            elif designation.lower().strip() == "staff":
                if wants_accommodation.upper() == "Y":
                    return "Staff cannot request for a livingspace!"
                else:
                    new_staff = Staff()
                    new_staff.name = name
                    new_staff.ID = self.getID("staff")
                    new_staff.office = self.assignOffice(new_staff.ID)
                    self.listOfStaffs.append(new_staff)
                    return new_staff
            else:
                return "Person cannot be created due to invalid designation!"
        else:
            return "Person cannot be created with an empty name!"

    def roomNameExist(self, room_name):
        found = False
        for i in range(0, len(self.all_rooms)):
            if self.all_rooms[i].name == room_name:
                return True
        return found

    def getID(self, designation):
        return ""

    def assignOffice(self, ID):
        return ""

    def assignLivingspace(staff, ID):
        return ""
