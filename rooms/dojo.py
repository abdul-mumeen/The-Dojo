from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace
import random
import string

class Dojo(object):
    def __init__(self):
        self.all_rooms = []
        self.staff_list = []
        self.fellow_list = []
        self.allocated = {}
        self.unallocated = {"office": [], "livingspace" : []}

    def create_room(self, room_name, room_type):
        log = ""
        if room_type.strip() != "" and len(room_name) > 0:
            if room_type == "office" or room_type == "livingspace":
                i = 0
                for room in room_name:
                    if room.strip() == "":
                        log += "\nThe " + room_type + " at index " + str(i) + " cannot be created due to empty name."
                    elif self.check_room_name_exist(room):
                        log += "\nThe " + room_type + " at index " + str(i) + " already existed."
                    else:
                        new_room = Office(room) if room_type == "office" else LivingSpace(room)
                        self.all_rooms.append(new_room)
                    i += 1
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
                fellow = self.add_fellow(name, wants_accommodation)
                self.fellow_list.append(fellow)
                #print("Fellow has been successfully added")
                return fellow
            elif designation.lower().strip() == "staff":
                if wants_accommodation.upper() == "Y":
                    return "Staff cannot request for a livingspace!"
                else:
                    staff = self.add_staff(name)
                    self.staff_list.append(staff)
                    return staff
                    #print("Staff has been successfully added")
            else:
                return "Person cannot be created due to invalid designation!"
        else:
            return "Person cannot be created with an empty name!"

    def add_fellow(self, name, accommodation):
        new_fellow = Fellow()
        new_fellow.name = name
        new_fellow.ID = self.get_id("fellow")
        new_fellow.office = self.allocate_room(new_fellow, Office)
        if accommodation.upper() == "Y":
            new_fellow.livingspace = self.allocate_room(new_fellow, LivingSpace)

        self.fellow_list.append(new_fellow)
        return new_fellow

    def add_staff(self, name):
        new_staff = Staff()
        new_staff.name = name
        new_staff.ID = self.get_id("staff")
        new_staff.office = self.allocate_room(new_staff, Office)
        self.staff_list.append(new_staff)
        return new_staff

    def check_room_name_exist(self, room_name):
        found = False
        for i in range(0, len(self.all_rooms)):
            if self.all_rooms[i].name == room_name:
                return True
        return found

    def get_available_rooms(self, room_type):
        available_room = []
        for room in self.all_rooms:
            if room.name in self.allocated:
                room_available = room.total_space > len(self.allocated[room.name])
            else:
                room_available = True
            if room_available != False and isinstance(room, room_type):
                available_room.append(room)
        return available_room

    def get_existing_id(self, person_list):
        id_list = []
        for i in range(0, len(person_list)):
            id_list.append(person_list[i].ID)
        return id_list

    def get_id(self, designation):
        if designation.lower == "fellow":
            id_exist = true
            fellow_id + ""
            while id_exist:
                fellow_id = "F-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                                      for _ in range(5))
                if not (fellow_id in get_existing_id(fellow_list)):
                    id_exist = False
            return fellow_id
        else:
            id_exist = True
            staff_id = ""
            while id_exist:
                staff_id = "S-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                                      for _ in range(5))
                if not (staff_id in self.get_existing_id(self.staff_list)):
                    id_exist = False
            return staff_id


    def allocate_room(self, person, room_type):

        available_room = self.get_available_rooms(room_type)
        if len(available_room) > 0:
            room = random.choice(available_room)
            if not room.name in self.allocated:
                self.allocated[room.name] = []

            self.allocated[room.name].append(person)
            return room.name
        else:
            if room_type == Office:
                self.unallocated["office"].append(person)
            else:
                self.unallocated["livingspace"].append(person)
                return ""

    def print_room(self, room_name):
        """" This function names of allocated members of the room """
        print_out = ""
        if room_name in self.allocated:
            for person in self.allocated[room_name]:
                print_out += person.name.upper() + "\n"
        else:
            print_out = "No allocation to this room"
        return print_out

    def print_allocation(self, file_name=None):
        """ This function print out all allocated rooms and their allocated members"""
        print_out = ""
        for room in self.allocated:
            names = ""
            for person in self.allocated[room]:
                names += person.name + ", "
            names = names[:-2]
            print_out += room + "\n" + ("-" * len(names)) + "\n" + names + "\n"
        if file_name is not None:
            file = open("data/%s" % file_name, "w" )
            file.write(print_out.upper())
            file.close()
        return print_out.upper()
