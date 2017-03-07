import sys
import os
from unittest import TestCase

from rooms.dojo import Dojo
from persons.staffs import Staff
from persons.fellows import Fellow
from persons.persons import Person
import re
ansi_escape = re.compile(r'\x1b[^m]*m')


class TestCreateRoom(TestCase):
    def setUp(self):
        self.ndojo = Dojo()

    def tearDown(self):
        self.ndojo.reset()

    def test_create_room_successfully(self):

        """
        This function test the successful
        creation of single type of room
        """
        initial_room_count = len(self.ndojo.all_rooms)
        self.assertEqual(initial_room_count, 0)
        blue_office = self.ndojo.create_room(["Blue"], "office")
        self.assertTrue(blue_office)
        new_room_count = len(self.ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_create_multiple_rooms_successfully(self):
        """
        This function test the successful
        creation of multiple rooms of a type
        """
        initial_room_count = len(self.ndojo.all_rooms)
        log = self.ndojo.create_room(["Blue", "Green", "Purple"], "office")
        self.assertTrue(log)
        new_room_count = len(self.ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 3)
        self.ndojo.create_room(["Yellow", "Brown", "Black"], "livingspace")
        latest_room_count = len(self.ndojo.all_rooms)
        self.assertEqual(latest_room_count - new_room_count, 3)

    def test_check_empty_input(self):
        """ This function test for empty room name and room type inputs """
        self.ndojo.create_room([], "  ")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(
            ansi_escape.sub("", log),
            "Cannot create rooms with empty room name and/or empty room type")

    def test_invalid_room_input(self):
        """ This function test for empty room name"""
        self.ndojo.create_room([" "], "office")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(
            ansi_escape.sub("", log),
            "The office at index 0 cannot be created due to empty room name.")

    def test_invalid_in_array_input(self):
        """ This function test for empty room name in array rooms"""
        self.ndojo.create_room(["Green", " ", "Black"], "livingspace")
        log = sys.stdout.getvalue().strip()
        log = log.split("\n")
        self.assertEqual(
            ansi_escape.sub("", log[len(log) - 1]),
            "The livingspace at index 1 cannot be created"
            " due to empty room name.")

    def test_invalid_room_type(self):
        """ This function test for invalid room type """
        self.ndojo.create_room(["Green", "Black"], "piper")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(
            ansi_escape.sub("", log),
            "Cannot create room(s), invalid room type enterred")

    def test_duplicate_office_name(self):
        """ This function test for creation of duplicate office names """
        self.ndojo.create_room(["Green", "Blue"], "office")
        self.ndojo.create_room(["Blue"], "office")
        log = sys.stdout.getvalue().strip()
        log = log.split("\n")
        self.assertEqual(
            ansi_escape.sub("", log[len(log) - 1]),
            "The office name 'Blue' already existed.")

    def test_duplicate_livingspace_name(self):
        """ This function test for creation of duplicate livingspace names """
        self.ndojo.create_room(
                    ["Brown", "Black", "Black"], "livingspace")
        log = sys.stdout.getvalue().strip()
        log = log.split("\n")
        self.assertEqual(
            ansi_escape.sub("", log[len(log) - 1]),
            "The livingspace name 'Black' already existed.")

    def test_alphanumeric_room_name(self):
        """ This function test for invalid alphanumeric livingspace name """
        self.ndojo.create_room(
                    ["Brown", "Bl9ck", "Black"], "livingspace")
        log = sys.stdout.getvalue().strip()
        log = log.split("\n")
        self.assertEqual(
            ansi_escape.sub("", log[len(log) - 1]),
            "Invalid livingspace name 'Bl9ck' supplied!")


class TestPrintFunctions(TestCase):
    def setUp(self):
        self.ndojo = Dojo()

    def tearDown(self):
        self.ndojo.reset()
        if os.path.isfile("data/test_file.txt"):
            os.remove("data/test_file.txt")

    def test_print_rooms(self):
        """ This function test the printing of rooms currently available """
        self.ndojo.print_rooms()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output), "No room added yet")
        self.ndojo.create_room(["Brown"], "office")
        self.ndojo.print_rooms()
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Brown - Office")

    def test_print_room(self):
        """ This function test the printing of names of occupant of a room """
        self.ndojo.create_room(["Brown"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        output_1 = sys.stdout.getvalue().strip() + "\n"
        self.ndojo.print_room("Brown")
        output_2 = sys.stdout.getvalue().strip()
        output = output_2.replace(output_1, "")
        self.assertEqual(ansi_escape.sub("", output), "BROWN" + "\n" +
                         ("-" * 30) + "\nHASSAN EL-SAHEED")

    def test_print_allocation_to_screen(self):
        """ This function test the printing of allocated persons to screen"""
        self.ndojo.create_room(["Blue"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.add_person("Mike Tyson", "staff")
        output_1 = sys.stdout.getvalue().strip() + "\n"
        self.ndojo.print_allocation()
        output_2 = sys.stdout.getvalue().strip()
        output = output_2.replace(output_1, "")
        self.assertEqual(
            ansi_escape.sub("", output)[:-2], "List not written to file,"
            " no file name supplied\nBLUE\n"
            "----------------------------\nHASSAN EL-SAHEED, MIKE TYSON")

    def test_print_list_of_staff(self):
        """ This function test the printing of list of staff """
        self.ndojo.print_person_list("fellow")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "This list is empty, no one has been added yet")
        new_fellow = self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.print_person_list("fellow")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 2]),
                         "{}\t\tHASSAN EL-SAHEED\t\t-\t\t-".format(
                            new_fellow.ID))

    def test_print_allocation_to_file(self):
        """ This function test the printing of allocated persons to file"""
        self.ndojo.create_room(["Blue"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_allocation("test_file")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[3][:-1], "HASSAN EL-SAHEED, MIKE TYSON")

    def test_print_unallocated_to_screen(self):
        """ This function test the printing of unallocated persons to screen"""
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_unallocated()
        output = sys.stdout.getvalue().strip()
        output = ansi_escape.sub("", output)
        self.assertEqual(output[len(output)-23:-1],
                         "MIKE TYSON - NO OFFICE")

    def test_print_unallocated_to_file(self):
        """ This function test the printing of unallocated persons to file"""
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_unallocated("test_file")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[3], "MIKE TYSON - NO OFFICE\n")


class TestAddPersons(TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def tearDown(self):
        self.dojo.reset()

    def test_add_staff(self):
        """ This function test for successful adding of staff """
        new_staff = self.dojo.add_person("Andy Carroll", "staff")
        self.assertIsInstance(new_staff, Staff)
        self.assertEqual(new_staff.name, "Andy Carroll")
        self.assertIsInstance(new_staff, Person)
        new_staff.print_me()
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Andy has been placed on a waiting list for office")

    def test_add_fellow(self):
        """ This function test for successful adding of fellow """
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        self.assertIsInstance(new_fellow, Fellow)
        self.assertEqual(new_fellow.name, "Jeremy Johnson")
        self.assertIsInstance(new_fellow, Person)
        self.assertEqual(new_fellow.livingspace, None)

    def test_add_fellow_allocate_to_room(self):
        """
        This function test for successful adding and
        allocation of fellow
        """
        self.dojo.create_room(["Idanre"], "office")
        new_fellow = self.dojo.add_person("Katwe Queen", "fellow", "Y")
        new_fellow.print_me()
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 2]),
                         "Katwe has been allocated the office Idanre")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Katwe has been placed on a waiting list for "
                         "livingspace")

    def test_add_person_livingspace_for_staff(self):
        """ This function checks for invalid inputs """
        self.dojo.add_person("Andy Carroll", "staff", "Y")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output),
                         "Staff cannot request for a livingspace!")

    def test_add_person_empty_name_supplied(self):
        self.dojo.add_person("  ", "staff")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output),
                         "Person cannot be created with an empty name!")

    def test_add_person_invalid_designation(self):
        self.dojo.add_person("Samora Dake", "type", "Y")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(
            ansi_escape.sub("", output),
            "Person cannot be created due to invalid designation!")


class TestReallocate(TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def tearDown(self):
        self.dojo.reset()

    def test_empty_valid_id(self):
        """ This function test for empty invalid id """
        self.dojo.reallocate_person(" ", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output), "Invalid id supplied")

    def test_wrong_format_invalid_id(self):
        """ This function test for wrong format invalid id """
        self.dojo.reallocate_person("asdff", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output), "Invalid id supplied")

    def test_wrong_invalid_id(self):
        """ This function test for wrong invalid id"""
        self.dojo.reallocate_person("A-FG4HU", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output), "Invalid id supplied")

    def test_rellocate_to_same_room(self):
        self.dojo.create_room(["Blue"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow")
        self.dojo.reallocate_person(new_fellow.ID, "Blue")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Fellow is currently assigned to this office")

    def test_fellow_not_existing_id(self):
        """ This function test for fellow existing id"""
        self.dojo.reallocate_person("F-GHJ7Y", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output),
                         "The id supplied is not found")

    def test_staff_not_existing_id(self):
        """ This function test for staff existing id"""
        self.dojo.reallocate_person("S-AS23Y", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(ansi_escape.sub("", output),
                         "The id supplied is not found")

    def test_room_exist(self):
        """ This function test if the room supplied exist"""
        self.dojo.create_room(["Blue"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]), "Room not found")

    def test_add_staff_to_livingspace(self):
        """ This function test staff rellocating to livingspace"""
        self.dojo.create_room(["Blue"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "staff")
        self.dojo.create_room(["Green"], "livingspace")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Staff cannot be moved to a livingspace")

    def test_fellow_office_reallocate(self):
        """ This function test if fellow office reallocation is successful"""
        self.dojo.create_room(["Green"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "N")
        self.dojo.create_room(["Brown"], "office")
        self.dojo.reallocate_person(new_fellow.ID, "Brown")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "Fellow has been successfully reallocated to office Brown")

    def test_staff_office_reallocate(self):
        """ This function test if staff office reallocation is successful"""
        self.dojo.create_room(["Green"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "staff")
        self.dojo.create_room(["Brown"], "office")
        self.dojo.reallocate_person(new_fellow.ID, "Brown")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "Staff has been successfully reallocated to office Brown")

    def test_fellow_livingspace_reallocate(self):
        """ This function test if fellow room reallocation is successful"""
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        self.dojo.create_room(["Brown"], "livingspace")
        self.dojo.reallocate_person(new_fellow.ID, "Brown")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Fellow has been"
                         " successfully reallocated to livingspace Brown")

    def test_fellow_livingspace(self):
        """ This function test if room rellocating to is of the same type"""
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "N")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "Fellow does not want a livingspace")

    def test_room_full(self):
        """ This function test when a room is full"""
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        new_fellow = self.dojo.add_person("Jeremy Parker", "fellow", "Y")
        new_fellow = self.dojo.add_person("Jeremy Henshaw", "fellow", "Y")
        new_fellow = self.dojo.add_person("Jeremy Crowell", "fellow", "Y")
        self.dojo.create_room(["Blue"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Python", "fellow", "Y")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "The room selected is full")


class TestLoadPeople(TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def tearDown(self):
        self.dojo.reset()
        if os.path.isfile("data/people.txt"):
            os.remove("data/people.txt")

    def test_file_empty(self):
        """ This function test if the file supplied is empty """
        file_content = ""
        file = open("data/people.txt", "w")
        file.write(file_content.upper())
        file.close()
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "The file selected is empty")

    def test_invalid_content(self):
        """ This function test if the file supplied contains invalid input """
        file_content = "OLUWAFEMI SULE FELLOW Y\n\
                        DOMINIC WALTERS STAFF Y\n\
                        SIMON PATTERSON FELLOW Y\n"
        file = open("data/people.txt", "w")
        file.write(file_content.upper())
        file.close()
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 3]),
            "Staff cannot request for a livingspace!")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "Some people on the list have been successfully loaded")

    def test_excess_parameters(self):
        """ This function test if the file supplied contains invalid input """
        file_content = "OLUWAFEMI SULE FELLOW Y\n\
                        DOMINIC WALTERS STAFF Y FREAK\n\
                        SIMON PATTERSON FELLOW Y\n"
        file = open("data/people.txt", "w")
        file.write(file_content.upper())
        file.close()
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 2]),
            "line 2 was not loaded because of invalid parameters supplied")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "Some people on the list have been successfully loaded")

    def test_load_successful(self):
        """ This function test file loaded successfully """
        file_content = "OLUWAFEMI SULE FELLOW Y\n\
                        DOMINIC WALTERS STAFF\n\
                        SIMON PATTERSON FELLOW Y\n\
                        MARI LAWRENCE FELLOW Y\n\
                        LEIGH RILEY STAFF\n\
                        TANA LOPEZ FELLOW Y\n\
                        KELLY McGUIRE STAFF"
        file = open("data/people.txt", "w")
        file.write(file_content.upper())
        file.close()
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
                ansi_escape.sub("", output[len(output) - 1]),
                "Everyone on the list have been successfully loaded")
        self.assertEqual(len(self.dojo.staff_list), 3)
        self.assertEqual(len(self.dojo.fellow_list), 4)

    def test_file_exist(self):
        """ This function test file existing or not"""
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "File not found")


class TestDatabase(TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room(["Blue", "Green"], "office")
        self.dojo.create_room(["Black", "Brown"], "livingspace")
        file_content = "OLUWAFEMI SULE FELLOW Y\n\
                        DOMINIC WALTERS STAFF\n\
                        SIMON PATTERSON FELLOW Y\n\
                        MARI LAWRENCE FELLOW Y\n\
                        LEIGH RILEY STAFF\n\
                        TANA LOPEZ FELLOW Y\n\
                        KELLY McGUIRE STAFF"
        file = open("data/people.txt", "w")
        file.write(file_content.upper())
        file.close()
        self.dojo.load_people("people")

    def tearDown(self):
        self.dojo.reset()
        if os.path.isfile("data/pressure.sqlite"):
            os.remove("data/pressure.sqlite")

    def test_save_state_named(self):
        """ This function test saving state with the name supplied """
        self.dojo.save_state("pressure")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "The state has been "
                         "successfully saved in pressure.sqlite")
        self.assertTrue(os.path.isfile("data/pressure.sqlite"))
        self.dojo.save_state("pressure")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "Database name already"
                         " existed! Kindly choose another name.")

    def test_save_state_unnamed(self):
        """ This function test saving state with the name generated """
        self.dojo.save_state("")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertGreaterEqual(ansi_escape.sub("", output[len(output) - 1]),
                                "The state has " +
                                "been successfully saved in 2017.sqlite")

    def test_load_state_file_not_exist(self):
        """ This function test if the file supplied exist """
        self.dojo.load_state("pressure")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(ansi_escape.sub("", output[len(output) - 1]),
                         "File not found")

    def test_load_state_successful(self):
        """
        This function test if the load state is successful
        when file exist
        """
        self.dojo.save_state("pressure")
        self.dojo.reset()
        self.dojo.load_state("pressure")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(
            ansi_escape.sub("", output[len(output) - 1]),
            "Data in pressure.sqlite have been successfully loaded")
        self.assertEqual(len(self.dojo.staff_list), 3)
        self.assertEqual(len(self.dojo.fellow_list), 4)
        self.assertEqual(len(self.dojo.all_rooms), 4)
        self.assertTrue("Green" in [room.name for room in self.dojo.all_rooms])
