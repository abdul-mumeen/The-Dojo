from unittest import TestCase
from rooms.dojo import Dojo

class TestCreatRoom(TestCase):
    def test_create_room_successfully(self):

        """ This function test the successful creation of single type of room """
        ndojo = Dojo()
        initial_room_count = len(ndojo.all_rooms)
        self.assertEqual(initial_room_count, 0)
        blue_office = ndojo.create_room(["Blue"], "office")
        self.assertTrue(blue_office)
        new_room_count = len(ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_create_multiple_rooms_successfully(self):
        """ This function test the successful creation of multiple rooms of a type """

        ndojo = Dojo()

        """ Returns True when successfully created the multiple rooms """
        initial_room_count = len(ndojo.all_rooms)
        log = ndojo.create_room(["Blue", "Green", "Purple"], "office")
        self.assertTrue(log)
        new_room_count = len(ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 3)
        ndojo.create_room(["Yellow", "Brown", "Black"], "livingspace")
        latest_room_count = len(ndojo.all_rooms)
        self.assertEqual(latest_room_count - new_room_count, 3)

    def test_check_invalid_input(self):
        """ This function test for invalid inputs """
        ndojo = Dojo()

        """ Returns error message instead of true with invalid inputs """
        log = ndojo.create_room([], "  ")
        self.assertEqual(log, "Cannot create rooms with empty room name and/or empty room type")
        log = ndojo.create_room([" "], "office")
        self.assertEqual(log, "\nThe office at index 0 cannot be created due to empty name.")
        log = ndojo.create_room(["Green", " ", "Black"], "livingspace")
        self.assertEqual(log, "\nThe livingspace at index 1 cannot be created due to empty name.")
        log = ndojo.create_room(["Green", "Black"], "piper")
        self.assertEqual(log, "\nCannot create room(s), invalid room type enterred")

    def test_check_duplicate_names(self):
        """ This function test for duplicate room names """
        ndojo = Dojo()

        """ Returns error message instead of true with duplicate values """
        log = ndojo.create_room(["Green", "Blue"], "office")
        log = ndojo.create_room(["Blue"], "office")
        self.assertEqual(log, "\nThe office at index 0 already existed.")
        log = ndojo.create_room(["Brown", "Black", "Black"], "livingspace")
        self.assertEqual(log, "\nThe livingspace at index 2 already existed.")

    def test_print_rooms(self):
        """ This function test the printing of names of occupant of a room """
        ndojo = Dojo()
        ndojo.create_room(["Brown"], "office")
        ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        name = ndojo.print_room("Brown")
        self.assertEqual(name, "HASSAN EL-SAHEED\n")

    def test_print_allocation(self):
        """ This function test the output from printing allocated persons """
        ndojo = Dojo()
        ndojo.create_room(["Blue"], "office")
        ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        ndojo.add_person("Mike Tyson", "staff")
        print_to_screen = ndojo.print_allocation()
        self.assertEqual(print_to_screen, "BLUE\n----------------------------\nHASSAN EL-SAHEED, MIKE TYSON\n")
        ndojo.print_allocation("test_file.txt")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[2][:-1], "HASSAN EL-SAHEED, MIKE TYSON")

    def test_print_unallocated(self):
        """ This function test the functin print_unallocated """
        ndojo = Dojo()
        #ndojo.add_person("Hassan El-Saheed", "fellow", "Y")
        ndojo.add_person("Mike Tyson", "staff")
        #ndojo.add_person("Abass Aminu", "fellow", "N")
        print_to_screen = ndojo.print_unallocated()
        self.assertEqual(print_to_screen, "MIKE TYSON - NO OFFICE\n")
                                            #+ "ABASS AMINU - NO OFFICE\n HASSAN EL-SAHEED - NO LIVINGSPACE\n")
        ndojo.print_unallocated("test_file.txt")
        file = open("data/test_file.txt", "r")
        names = file.readlines()
        file.close()
        self.assertEqual(names[0],"MIKE TYSON - NO OFFICE\n")
