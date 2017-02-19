from unittest import TestCase
from rooms.dojo import Dojo
import sys

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
        self.ndojo.create_room([], "  ")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(log, \
            "Cannot create rooms with empty room name and/or empty room type")

    def test_invalid_room_input(self):
        """ This function test for empty room name"""
        self.ndojo.create_room([" "], "office")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(log, \
            "The office at index 0 cannot be created due to empty name.")

    def test_invalid_in_array_input(self):
        """ This function test for empty room name in array rooms"""
        self.ndojo.reset()
        self.ndojo.create_room(["Green", " ", "Black"], "livingspace")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(log, \
           "The livingspace at index 1 cannot be created due to empty name.")

    def test_invalid_room_type(self):
        """ This function test for invalid room type """
        self.ndojo.create_room(["Green", "Black"], "piper")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(log, \
            "Cannot create room(s), invalid room type enterred")

    def test_duplicate_office_name(self):
        """ This function test for creation of duplicate office names """
        self.ndojo.reset()
        self.ndojo.create_room(["Green", "Blue"], "office")
        self.ndojo.create_room(["Blue"], "office")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(log, "The office at index 0 already existed.")

    def test_duplicate_livingspace_name(self):
        """ This function test for creation of duplicate livingspace names """
        self.ndojo.create_room(\
                    ["Brown", "Black", "Black"], "livingspace")
        log = sys.stdout.getvalue().strip()
        self.assertEqual(log, "The livingspace at index 2 already existed.")

    def test_print_rooms(self):
        """ This function test the printing of names of occupant of a room """
        self.ndojo.reset()
        self.ndojo.create_room(["Brown"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.print_room("Brown")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "BROWN" + "\n" + ("-" * 15) + "\n" + \
                                                "HASSAN EL-SAHEED")

    def test_print_allocation_to_screen(self):
        """ This function test the printing of allocated persons to screen"""
        self.ndojo.reset()
        self.ndojo.create_room(["Blue"], "office")
        self.ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_allocation()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "BLUE\n" + \
            "----------------------------\nHASSAN EL-SAHEED, MIKE TYSON")

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
        self.ndojo.print_unallocated()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output[len(output)-22:], "MIKE TYSON - NO OFFICE")

    def test_print_unallocated_to_file(self):
        """ This function test the printing of unallocated persons to file"""
        self.ndojo.reset()
        self.ndojo.add_person("Mike Tyson", "staff")
        self.ndojo.print_unallocated("test_file")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[2],"MIKE TYSON - NO OFFICE\n")
