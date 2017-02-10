from persons.staffs import Staff
from persons.fellows import Fellow


class Persons(object):
    def __init__(self):
        self.listOfStaffs = []
        self.listOfFellows = []

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

    def getID(self, designation):
        return ""

    def assignOffice(self, ID):
        return ""

    def assignLivingspace(staff, ID):
        return ""
