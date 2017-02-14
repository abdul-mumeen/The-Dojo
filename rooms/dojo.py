from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace
import random
import string


class Dojo(object):
    """This is the app main class that calls all the functions"""
    def __init__(self):
        self.all_rooms = {}
        self.staff_list = []
        self.fellow_list = []
        self.allocated = {}
        self.unallocated = {"office": [], "livingspace" : []}

    def create_room(self, room_name, room_type):
        """
        This function create a single room or multiple rooms of the same type
        by receiving an array of room names an the room type.
        """
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
                        self.all_rooms[new_room.name] = new_room

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
        """
        This function add a person by calling the add_fellow
        or add_staff function as the case may be.
        """
        if name.strip() != "":
            if designation.lower().strip() == "fellow":
                fellow = self.add_fellow(name, wants_accommodation)
                return fellow
            elif designation.lower().strip() == "staff":
                if wants_accommodation.upper() == "Y":
                    return "Staff cannot request for a livingspace!"
                else:
                    staff = self.add_staff(name)
                    return staff
            else:
                return "Person cannot be created due to invalid designation!"
        else:
            return "Person cannot be created with an empty name!"

    def add_fellow(self, name, accommodation):
        """
        This function create a fellow and add it to the list of staff
        while calling the allocate function to allocate room.
        """
        new_fellow = Fellow(name, "fellow")
        new_fellow.generate_id("fellow", self.fellow_list)
        new_fellow.office = self.allocate_room(new_fellow, Office)
        if accommodation.upper() == "Y":
            new_fellow.livingspace = self.allocate_room(new_fellow, LivingSpace)
            new_fellow.wants_accommodation = True
        self.fellow_list.append(new_fellow)
        return new_fellow

    def add_staff(self, name):
        """
        This function create a staff and add it to the list of staff
        while calling the allocate function to allocate room.
        """
        new_staff = Staff(name, "staff")
        new_staff.generate_id("staff", self.staff_list)
        new_staff.office = self.allocate_room(new_staff, Office)
        self.staff_list.append(new_staff)
        return new_staff

    def check_room_name_exist(self, room_name):
        """
        This function checks if a room name passed already existed
        in the list of all rooms.
        """
        return room_name in self.all_rooms
        # found = False
        # for room in self.all_rooms:
        #     if room == room_name:
        #         return True
        # return found

    def get_available_rooms(self, room_type):
        """
        This function gets the list of availble rooms
        of a specified room type
        """
        available_room = []
        for room in self.all_rooms:
            room_available = self.all_rooms[room].total_space > \
                                            len(self.allocated[room]) \
                                            if room in self.allocated else True
            # if room in self.allocated:
            #     room_available = self.all_rooms[room].total_space > \
            #                                     len(self.allocated[room])
            # else:
            #     room_available = True
            if room_available != False and \
                        isinstance(self.all_rooms[room], room_type):
                available_room.append(self.all_rooms[room])
        return available_room


    def allocate_room(self, person, room_type):
        """
        This function randomly assign room to a person
        from a list of rooms that are available_room
        """
        available_rooms = self.get_available_rooms(room_type)
        if len(available_rooms) > 0:
            room = random.choice(available_rooms)
            if not room.name in self.allocated:
                self.allocated[room.name] = []
            self.allocated[room.name].append(person)
            return room
        else:
            if room_type == Office:
                self.unallocated["office"].append(person)
            else:
                self.unallocated["livingspace"].append(person)
            return ""

    def print_room(self, room_name):
        """"
        This function prints names of all allocated
        members of the passed room
        """
        print_out = ""
        if room_name in self.allocated:
            for person in self.allocated[room_name]:
                print_out += person.name.upper() + "\n"
        else:
            print_out = "No allocation to this room"
        return print_out

    def print_allocation(self, file_name=None):
        """
        This function prints out all allocated rooms
        and their allocated members
        """
        print_out = ""
        for room in self.allocated:
            names = ""
            for person in self.allocated[room]:
                names += person.name + ", "
            names = names[:-2]
            print_out += room + "\n" + ("-" * len(names)) + \
                         "\n" + names + "\n"
        if print_out == "":
            return "Nobody on the allocated list."
        else:
            self.write_to_file(print_out, file_name)
            return print_out.upper()

    def print_unallocated(self, file_name=None):
        """ This function prints the list of unallocated persons"""
        print_out = ""
        for key in self.unallocated:
            for person in self.unallocated[key]:
                print_out += person.name.upper() + " - NO " + \
                                            key.upper() + "\n"
        if print_out == "":
            return "Nobody on the unallocated list."
        else:
            self.write_to_file(print_out, file_name)
            return print_out.upper()

    def write_to_file(self, print_out, file_name):
        """ This function write a string to the file_name specified"""
        if file_name is not None:
            file = open("data/%s" % file_name, "w" )
            file.write(print_out.upper())
            file.close()
            print ("List have been successfuly written to file")
