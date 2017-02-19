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
            if room_type.lower() == "office" or \
                                        room_type.lower() == "livingspace":
                i = 0
                for room in room_name:
                    if room.strip() == "":
                        log += "\nThe {} at index {} ".format(room_type, \
                            str(i)) + "cannot be created due to empty name."
                    elif self.check_room_name_exist(room):
                        log += "\nThe {} at index {} ".format(room_type, \
                            str(i)) + "already existed."
                    else:
                        self.add_room(room, room_type)
                    i += 1
            else:
                log += "\nCannot create room(s), invalid room type enterred"
        else:
            log += "Cannot create rooms with empty " + \
                                    "room name and/or empty room type"
        if log == "":
            return True
        else:
            print(log)

    def add_room(self, room_name, room_type):
        new_room = None
        if room_type == "office":
            new_room = Office(room_name)
            print("An office called {} ".format(room_name) + \
                                            "has been successfully created")
        else:
            new_room = LivingSpace(room_name)
            room_name = room_name.title()
            print("A livingspace called {} ".format(room_name) + \
                                            "has been successfully created")
        self.all_rooms[new_room.name] = new_room


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
                    print("Staff cannot request for a livingspace!")
                else:
                    staff = self.add_staff(name)
                    return staff
            else:
                print("Person cannot be created due to invalid designation!")
        else:
            print("Person cannot be created with an empty name!")

    def add_fellow(self, name, accommodation):
        """
        This function create a fellow and add it to the list of staff
        while calling the allocate function to allocate room.
        """
        new_fellow = Fellow(name, "fellow")
        new_fellow.generate_id("fellow", self.fellow_list)
        new_fellow.office = self.allocate_room(new_fellow, Office)
        if accommodation.upper() == "Y":
            new_fellow.livingspace = self.allocate_room(new_fellow, \
                                                            LivingSpace)
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
        print_out = room_name.upper() + "\n" + ("-" * 15) + "\n" + print_out
        print(print_out)

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
            print("Nobody on the allocated list.")
        else:
            self.write_to_file(print_out, file_name)
            print(print_out.upper())

    def print_unallocated(self, file_name=None):
        """ This function prints the list of unallocated persons"""
        print_out = ""
        for key in self.unallocated:
            for person in self.unallocated[key]:
                print_out += person.name.upper() + " - NO " + \
                                            key.upper() + "\n"
        if print_out == "":
            print("Nobody on the unallocated list.")
        else:
            print_out = "UNALLOCATED LIST\n\n" + print_out
            self.write_to_file(print_out, file_name)
            print(print_out.upper())

    def write_to_file(self, print_out, file_name):
        """ This function write a string to the file_name specified"""
        if file_name is not None:
            file = open("data/%s.txt" % file_name, "w" )
            file.write(print_out.upper())
            file.close()
            print("List have been successfully written to file")

    def reset(self):
        """ This function reset Dojo to it initializatio stage"""
        self.__init__()

    def check_valid_id(self, input_val):
        """ this function checks validity of the id supplied"""
        valid_string = string.ascii_uppercase + string.digits + "-"
        output = False if input_val.strip() == "" or \
                not set(input_val.upper()).issubset(set(valid_string)) or \
                                input_val.upper()[0] not in ["F", "S"] or \
                                        len(input_val) != 7 \
                                            else True
        return output

    def get_person_list_index(self, person_id):
        """ This function gets the index of the person_id on
            the staff list or fellow list
        """
        index = -1
        person_list = self.fellow_list if person_id.upper()[0] == "F" \
                                                    else self.staff_list
        for i in range(len(person_list)):
            if person_list[i].ID.upper() == person_id.upper():
                index = i
                break
        return index


    def reallocate_person(self, person_id, new_room_name):
        """ This function reallocate a person to a supplied room """
        if self.check_valid_id(person_id):
            id_index = self.get_person_list_index(person_id)
            if id_index > -1:
                if new_room_name in self.all_rooms:
                    if not new_room_name in self.allocated:
                        self.move_person(person_id, id_index, new_room_name)
                    elif self.all_rooms[new_room_name].total_space > \
                            len(self.allocated[new_room_name]):
                        self.move_person(person_id, id_index, new_room_name)
                    else:
                        print("The room selected is full")
                else:
                    print("Room not found")
            else:
                print("The id supplied is not found")
        else:
            print("Invalid id supplied")


    def move_person(self, person_id, index, new_room_name):
        """ This function move a person to the new room"""
        if isinstance(self.all_rooms[new_room_name], LivingSpace) and \
                    person_id.upper()[0] == "S":
            print("Staff cannot be moved to a livingspace")
        elif isinstance(self.all_rooms[new_room_name], LivingSpace):
            if self.fellow_list[index].wants_accommodation:
                if self.fellow_list[index].livingspace != None:
                    self.remove_from_allocated(person_id)
                self.fellow_list[index].livingspace = \
                                    self.all_rooms[new_room_name]
                self.add_room_to_alloacted(new_room_name)
                self.allocated[new_room_name].append(self.fellow_list[index])
                print("Fellow has been successfully " + \
                                    "moved to the new livingspace")
            else:
                print("Fellow does not want a livingspace")
        else:
            if person_id.upper()[0] == "S":
                if self.staff_list[index].office != None:
                    self.remove_from_allocated(person_id)
                self.staff_list[index].office = self.all_rooms[new_room_name]
                self.add_room_to_alloacted(new_room_name)
                self.allocated[new_room_name].append(self.staff_list[index])
                print("Staff has been successfully moved to the new office")
            else:
                if self.fellow_list[index].livingspace != None:
                    self.remove_from_allocated(person_id)
                self.fellow_list[index].office = self.all_rooms[new_room_name]
                self.add_room_to_alloacted(new_room_name)
                self.allocated[new_room_name].append(self.fellow_list[index])
                print("Fellow has been successfully moved to the new office")

    def add_room_to_alloacted(self, room_name):
        """ this function add a new room to the room allocated list """
        if not room_name in self.allocated:
            self.allocated[room_name] = []

    def remove_from_allocated(self, person_id):
        """ this function remove a person from previously allocated room"""
        for key in self.allocated:
            for i in range(len(self.allocated[key])):
                if self.allocated[key][i].ID.upper() == person_id.upper():
                    self.allocated[key].pop(i)
                    return True
