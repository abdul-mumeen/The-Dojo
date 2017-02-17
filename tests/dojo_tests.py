from unittest import TestCase
from rooms.dojo import Dojo

class TestCreatRoom(TestCase):
    ndojo = Dojo()
    def test_create_room_successfully(self):

        """
        This function test the successful
        creation of single type of room
        """
        self.ndojo.reset()
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
        self.ndojo.reset()
        """ Returns True when it successfully creates the multiple rooms """
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
        log = self.ndojo.create_room([], "  ")
        self.assertEqual(log, \
            "Cannot create rooms with empty room name and/or empty room type")

    def test_invalid_room_input(self):
        log = self.ndojo.create_room([" "], "office")
        self.assertEqual(log, \
            "\nThe office at index 0 cannot be created due to empty name.")

    def test_invalid_in_array_input(self):
        log = self.ndojo.create_room(["Green", " ", "Black"], "livingspace")
        self.assertEqual(log, \
           "\nThe livingspace at index 1 cannot be created due to empty name.")

    def test_invalid_room_type(self):
        log = self.ndojo.create_room(["Green", "Black"], "piper")
        self.assertEqual(log, \
            "\nCannot create room(s), invalid room type enterred")

    def test_check_duplicate_names(self):
        """ This function test for creation of duplicate room names """

        log = self.ndojo.create_room(["Green", "Blue"], "office")
        log = self.ndojo.create_room(["Blue"], "office")
        self.assertEqual(log, "\nThe office at index 0 already existed.")
        log = self.ndojo.create_room(\
                    ["Brown", "Black", "Black"], "livingspace")
        self.assertEqual(log, "\nThe livingspace at index 2 already existed.")

    def test_print_rooms(self):
        """ This function test the printing of names of occupant of a room """
        self.ndojo.reset()
        self.ndojo.create_room(["Brown"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        name = self.ndojo.print_room("Brown")
        self.assertEqual(name, "HASSAN EL-SAHEED\n")

    def test_print_allocation_to_screen(self):
        """ This function test the printing of allocated persons to screen"""
        self.ndojo.reset()
        self.ndojo.create_room(["Blue"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.add_person("Mike Tyson", "staff")
        print_to_screen = self.ndojo.print_allocation()
        self.assertEqual(print_to_screen, "BLUE\n" + \
            "----------------------------\nHASSAN EL-SAHEED, MIKE TYSON\n")

    def test_print_allocation_to_file(self):
        """ This function test the printing of allocated persons to file"""
        self.ndojo.reset()
        self.ndojo.create_room(["Blue"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_allocation("test_file")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[2][:-1], "HASSAN EL-SAHEED, MIKE TYSON")

    def test_print_unallocated_to_screen(self):
        """ This function test the printing of unallocated persons to screen"""
        self.ndojo.reset()
        self.ndojo.add_person("Mike Tyson", "staff")
        print_to_screen = self.ndojo.print_unallocated()
        self.assertEqual(print_to_screen, "MIKE TYSON - NO OFFICE\n")

    def test_print_unallocated_to_file(self):
        """ This function test the printing of unallocated persons to file"""
        self.ndojo.reset()
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_unallocated("test_file")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[0],"MIKE TYSON - NO OFFICE\n")
