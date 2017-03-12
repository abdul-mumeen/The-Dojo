import os
import random
import string

from termcolor import cprint

from data.database import DB
from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace
from utils.custom_messages import *


class Dojo(object):
    """This is the app main class that has most functions"""

    def __init__(self):
        self.all_rooms = []
        self.staff_list = []
        self.fellow_list = []
        self.allocated = {}
        self.unallocated = {"office": [], "livingspace": []}

    def create_room(self, room_name, room_type):
        """
        This function create a single room or multiple rooms of the same type
        by receiving an array of room names an the room type.
        """
        log = ""
        if room_type.lower() in ["office", "livingspace"]:
            for room in room_name:
                room = room.title()
                if not room.isalpha() or room in ["Office", "Livingspace"]:
                    log += invalid_room_name_error.format(
                        room_type, room.capitalize())
                elif self.check_room_name_exist(room):
                    log += room_exist_error.format(room_type, room)
                else:
                    self.add_room(room, room_type)
        else:
            log = invalid_room_type_error

        cprint(log, "red")

    def add_room(self, room_name, room_type):
        """ This function add the new room to the list of all rooms"""
        new_room = None
        if room_type.lower() == "office":
            new_room = Office(room_name)
            cprint(office_created.format(room_name), "green")
            self.all_rooms.append(new_room)
        else:
            new_room = LivingSpace(room_name)
            cprint(livingspace_created.format(room_name), "green")
            self.all_rooms.append(new_room)

    def add_person(self, name, designation, wants_accommodation="N"):
        """
        This function add a person by calling the add_fellow
        or add_staff function as the case may be.
        """
        wants_accommodation = wants_accommodation.lower()
        if wants_accommodation in ["yes", "y", "no", "n"]:
            if designation.lower() == "fellow":
                return self.add_fellow(name, wants_accommodation)
            elif designation.lower().strip() == "staff":
                if wants_accommodation in ["y", "yes"]:
                    cprint(livingspace_request_error, "red")
                else:
                    return self.add_staff(name)
            else:
                cprint(invalid_designation_error, "red")
        else:
            cprint(invalid_wants_accomodation, "red")

    def add_fellow(self, name, accommodation):
        """
        This function create a fellow and add it to the list of fellow
        while calling the allocate function to allocate room.
        """
        new_fellow = Fellow(name)
        new_fellow.generate_id(self.fellow_list)
        new_fellow.office = self.allocate_room(new_fellow, Office)
        if accommodation in ("y", "yes"):
            new_fellow.livingspace = self.allocate_room(new_fellow,
                                                        LivingSpace)
            new_fellow.wants_accommodation = 1
        self.fellow_list.append(new_fellow)
        return new_fellow

    def add_staff(self, name):
        """
        This function create a staff and add it to the list of staff
        while calling the allocate function to allocate room.
        """
        new_staff = Staff(name, "staff")
        new_staff.generate_id(self.staff_list)
        new_staff.office = self.allocate_room(new_staff, Office)
        self.staff_list.append(new_staff)
        return new_staff

    def check_room_name_exist(self, room_name):
        """
        This function checks if a room name passed already existed
        in the list of all rooms.
        """
        return room_name in [room.name for room in self.all_rooms]

    def get_available_rooms(self, room_type):
        """
        This function gets the list of availble rooms
        of a specified room type
        """
        available_room = []
        for room in self.all_rooms:
            room_available = (
                room.total_space > len(self.allocated[room.name])
                if room.name in self.allocated else True
            )

            if room_available and isinstance(room, room_type):
                available_room.append(room)
        return available_room

    def allocate_room(self, person, room_type):
        """
        This function randomly assign room to a person
        from a list of rooms that are available_room
        """
        rooms_mapping = {Office: "office", LivingSpace: "livingspace"}
        available_rooms = self.get_available_rooms(room_type)
        if available_rooms:
            room = random.choice(available_rooms)
            if room.name not in self.allocated:
                self.allocated[room.name] = []
            self.allocated[room.name].append(person)
            return room
        else:
            self.unallocated[rooms_mapping[room_type]].append(person.ID)

    def print_room(self, room_name):
        """"
        This function prints names of all allocated
        members of the passed room
        """
        print_out = ""
        room_name = room_name.title()
        if room_name in [room.name for room in self.all_rooms]:
            if room_name in {room for room in self.allocated}:
                print_out = "\n".join(
                    [person.name.upper()
                     for person in self.allocated[room_name]])
            else:
                print_out = "No allocation for this room"
            print_out = room_name.upper() + "\n" + ("-" * 30) + "\n" + \
                print_out
        else:
            print_out = "No such room as " + room_name
        cprint(print_out, "green")

    def print_allocation(self, file_name=None):
        """
        This function prints out all allocated rooms
        and their allocated members
        """
        print_out = ""
        for room in self.allocated:
            names = []
            for person in self.allocated[room]:
                names.append(person.name)
            names = ", ".join(names)
            print_out += "\n".join([room, ("-" * len(names)), names, "\n"])
        if not print_out:
            cprint(empty_allocation_list, "yellow")
        else:
            self.write_to_file(print_out, file_name)
            cprint(print_out.upper(), "green")

    def print_rooms(self):
        """ This function prints out all available rooms """
        room_type_mapping = {Office: "Office", LivingSpace: "Livingspace"}
        room_names = []
        for room in self.all_rooms:
            room_names.append(
                " - ".join([room.name, room_type_mapping[type(room)]]))
        room_names = "\n".join(room_names)
        if not room_names:
            cprint(empty_room_list, "yellow")
        else:
            cprint("List of all rooms\n" + room_names, "green")

    def print_unallocated(self, file_name=None):
        """ This function prints the list of unallocated persons"""
        print_out = ""
        for key in self.unallocated:
            for id in self.unallocated[key]:
                person = [person for person in
                          (self.staff_list + self.fellow_list)
                          if person.ID.upper() == id.upper()][0]
                print_out += person.name.upper() + " - NO " + \
                    key.upper() + "\n"
        if not print_out:
            cprint(empty_unallocated_list, "yellow")
        else:
            print_out = "UNALLOCATED LIST\n\n" + print_out
            self.write_to_file(print_out, file_name)
            cprint(print_out.upper(), "green")

    def write_to_file(self, print_out, file_name):
        """ This function write a string to the file_name specified"""
        if file_name:
            if os.path.isfile("data/%s.txt" % file_name):
                option = ""
                cprint(file_exist_error, "yellow")
                cprint(file_operation_menu, "yellow")
                while option.lower() not in ["a", "w", "c"]:
                    option = input("a, w or c: ")
                self.execute_write_to_file(
                    print_out, file_name, option.lower())
            else:
                self.execute_write_to_file(print_out, file_name, "w")
        else:
            cprint(empty_file_name_info, "green")

    def execute_write_to_file(self, print_out, file_name, option):
        option_mapping = {"a": "appended", "w": "written"}
        if option == "c":
            cprint(file_cancelled_message, "yellow")
        else:
            file = open("data/%s.txt" % file_name, "{}".format(option))
            file.write("\n" + print_out.upper())
            file.close()
            cprint(write_to_file_success.format(option_mapping[option],
                                                file_name), "green")

    def reset(self):
        """ This function reset Dojo to it initializatio stage"""
        self.__init__()

    def check_valid_id(self, input_val):
        """ This function checks validity of the id supplied.
        It checks if it contains only '-', numbers and alphabets
        It confirms that the first letter is either F for fellows
        or S for staffs
        """
        valid_string = string.ascii_uppercase + string.digits + "-"
        input_val = input_val.upper()
        output = False if not input_val.strip() or \
            not set(input_val).issubset(set(valid_string)) or \
            input_val[0] not in ["F", "S"] or \
            len(input_val) != 7 else True
        return output

    def get_person(self, person_id):
        """ This function gets the index of the person_id on
            the staff list or fellow list
        """

        person_list = (
            self.fellow_list if person_id.startswith('F') else self.staff_list
        )
        for index, person in enumerate(person_list):
            if person_id == person.ID:
                return person
        else:
            return None

    def reallocate_person(self, person_id, new_room_name):
        """ This function reallocates a person to a given room. """
        person_id = person_id.upper()
        if self.check_valid_id(person_id):
            person = self.get_person(person_id)
            if person:
                new_room_name = new_room_name.title()
                if new_room_name in [room.name for room in self.all_rooms]:
                    room = [room for room in self.all_rooms if room.name ==
                            new_room_name][0]
                    if new_room_name not in self.allocated or \
                            room.total_space > \
                            len(self.allocated[new_room_name]):
                        self.move_person(person, new_room_name)
                    else:
                        cprint(room_full_error, "yellow")
                else:
                    cprint("Room not found", "red")
            else:
                cprint(missing_id_error, "red")
        else:
            cprint(invalid_id, "red")

    def move_person(self, person_obj, new_room_name):
        """ This function move a person to the new room"""
        person_id = person_obj.ID
        person = "Staff" if person_id.startswith("S") else "Fellow"
        room = [room for room in self.all_rooms if room.name ==
                new_room_name][0]
        if isinstance(room, LivingSpace) and person_id.startswith("S"):
            cprint(staff_livingspace_error, "red")
        else:
            room_type_attr_mapping = {True: "livingspace", False: "office"}
            room_instance_mapping = {
                "office": Office, "livingspace": LivingSpace
            }
            room_type = ""
            if isinstance(room, LivingSpace):
                if person_obj.wants_accommodation:
                    room_type = room_type_attr_mapping[True]
                else:
                    cprint(livingspace_not_request, "red")
                    return
            else:
                room_type = room_type_attr_mapping[False]

            if getattr(person_obj, room_type):
                current_room = getattr(person_obj, room_type)
                if current_room.name != new_room_name:
                    self.remove_from_allocated(
                        person_id, room_instance_mapping[room_type])
                else:
                    cprint(same_room_error.format(person, room_type), "yellow")
                    return
            setattr(person_obj, room_type, room)
            self.add_room_to_allocated(new_room_name)
            if person_id in self.unallocated[room_type]:
                self.unallocated[room_type].remove(person_id)
            self.allocated[new_room_name].append(person_obj)
            cprint(room_reallocate_success.format(person, room_type) +
                   new_room_name, "green")

    def add_room_to_allocated(self, room_name):
        """ this function add a new room to the room allocated list """
        if room_name.title() not in self.allocated:
            self.allocated[room_name.title()] = []

    def remove_from_allocated(self, person_id, room_type):
        """ This function remove a person from previously allocated room"""
        person = next((person for person in self.staff_list + self.fellow_list
                       if person.ID.upper() == person_id.upper()), None)
        if person:
            key = person.office.name.title() if room_type == Office else \
                person.livingspace.name.title()
            self.allocated[key].remove(person)
            return True

    def print_person_list(self, staff_or_fellow):
        """This function print a list of staff or fellow and their details"""
        person_mapping = {"staff": [self.staff_list, "Staff List\n"],
                          "fellow": [self.fellow_list, "Fellow List\n"]}
        person_list, list_header = person_mapping[staff_or_fellow]

        list_header += "ID\t\tNAME\t\tOFFICE NAME\tLIVINGSPACE\n"
        print_out = list_header + ("-" * 70) + "\n"
        for person in person_list:
            office_name = person.office.name if person.office else "-"
            livingspace_name = person.livingspace.name \
                if staff_or_fellow == "fellow" and person.livingspace else "-"
            print_out += "{}\t\t{}\t\t{}\t\t{}\n".format(
                person.ID, person.name.upper(), office_name.upper(),
                livingspace_name.upper())
        if len(print_out) > 125:
            cprint(print_out, "green")
        else:
            cprint(empty_person_list, "yellow")

    def get_file_content(self, file_name):
        if os.path.isfile("data/{}.txt".format(file_name)):
            file = open("data/{}.txt".format(file_name), "r")
            content = file.read()
            file.close()
            if content.strip():
                content = content.split("\n")
                return content
            else:
                cprint(empty_file_error, "yellow")
        else:
            cprint("File not found", "yellow")

    def load_people(self, file_name):
        content = self.get_file_content(file_name)
        error = 0
        if not content:
            return
        for index, person_detail in enumerate(content):
            if person_detail.strip():
                person_detail = person_detail.strip().split()
                name = person_detail[0] + " " + person_detail[1]
                if len(person_detail) in [3, 4]:
                    person_detail.append("N")\
                        if len(person_detail) == 3 else person_detail
                    person = self.add_person(name, person_detail[2],
                                             person_detail[3])
                    if not person:
                        cprint(line_not_loaded_error.format(index + 1), "red")
                        error += 1
                else:
                    cprint(line_parameter_error.format(index + 1), "red")
                    error += 1
        self.print_load_people_message(error, content)

    def print_load_people_message(self, error, content):
        response_mapping = ["Everyone", "Some people", "Nobody"]
        if error:
            error = 2 if error >= len(content) - 1 else 1
        load_ran = response_mapping[error]
        cprint(people_loaded_info.format(load_ran), "green")

    def save_state(self, db_name):
        """
        This function save state by storing data from the
        application's data structure into a database
        """
        db_name = "" if not db_name else db_name
        new_db = DB()
        person_list = self.staff_list + self.fellow_list
        log = new_db.save_state(db_name, self.all_rooms, person_list)
        cprint(log, "yellow")

    def load_state(self, db_name):
        """
        This function retrieves data from the database and assign them
        to the appropraite variables to store them
        """
        if os.path.isfile("data/{}.sqlite".format(db_name)):
            self.reset()
            new_db = DB()
            app_data = new_db.load_state(db_name)
            self.all_rooms = app_data["all_rooms"]
            self.staff_list = app_data["staff_list"]
            self.fellow_list = app_data["fellow_list"]
            allocations = self.get_allocations()
            self.allocated = allocations["allocated"]
            self.unallocated = allocations["unallocated"]
            cprint(state_loaded_info.format(db_name), "green")
        else:
            cprint("File not found", "yellow")

    def get_allocations(self):
        """
        This function extracts the allocated and unallocated
        collection from the data retrieved from the database
        """
        allocated = {}
        unallocated = {"office": [], "livingspace": []}
        for person in (self.staff_list + self.fellow_list):
            office = person.office
            if office:
                office_name = office.name.title()
                if office_name not in allocated:
                    allocated[office_name] = []
                allocated[office_name].append(person)
            else:
                unallocated["office"].append(person.ID)
            if hasattr(person, "livingspace"):
                livingspace = person.livingspace
                if livingspace:
                    livingspace_name = livingspace.name.title()
                    if livingspace_name not in allocated:
                        allocated[livingspace_name] = []
                    allocated[livingspace_name].append(person)
                else:
                    if person.wants_accommodation:
                        unallocated["livingspace"].append(person.ID.upper())
        return {"allocated": allocated, "unallocated": unallocated}
