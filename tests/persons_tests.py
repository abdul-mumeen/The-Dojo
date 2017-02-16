from unittest import TestCase
from rooms.dojo import Dojo
from persons.staffs import Staff
from persons.fellows import Fellow
from persons.persons import Person

class TestPersons(TestCase):
    dojo = Dojo()
    def test_add_staff(self):
        """ This function test for successful adding of staff """
        new_staff = self.dojo.add_person("Andy Carroll", "staff")
        self.assertIsInstance(new_staff, Staff)
        self.assertEqual(new_staff.name, "Andy Carroll")
        self.assertIsInstance(new_staff, Person)

    def test_add_fellow(self):
        """ This function test for successful adding of fellow """
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        self.assertIsInstance(new_fellow, Fellow)
        self.assertEqual(new_fellow.name, "Jeremy Johnson")
        self.assertIsInstance(new_fellow, Person)
        self.assertEqual(new_fellow.livingspace, "")

    def test_add_person_invalid_input(self):
        """ This function checks for invalid inputs """
        new_staff = self.dojo.add_person("Andy Carroll", "staff", "Y")
        self.assertEqual(new_staff, "Staff cannot request for a livingspace!")
        new_staff = self.dojo.add_person("  ", "staff")
        self.assertEqual(new_staff, \
                    "Person cannot be created with an empty name!")
        new_staff = self.dojo.add_person("Samora Dake", "type", "Y")
        self.assertEqual(new_staff, \
                    "Person cannot be created due to invalid designation!")

    def test_valid_fellow_id(self):
        """ this function test for invalid fellow id"""
        print_out = self.dojo.rellocate(" ", "Blue")
        self.assertEqual(print_out, "Invalid fellow id")
        print_out = self.dojo.rellocate("asdff", "Blue")
        self.assertEqual(print_out, "Invalid fellow id")
        print_out = self.dojo.rellocate("A-FG4HU", "Blue")
        self.assertEqual(print_out, "Invalid fellow id")

    def test_valid_staff_id(self):
        """ this function test for invalid staff id"""
        print_out = self.dojo.rellocate(" ", "Blue")
        self.assertEqual(print_out, "Invalid staff id")
        print_out = self.dojo.rellocate("aswdf", "Blue")
        self.assertEqual(print_out, "Invalid staff id")
        print_out = self.dojo.rellocate("A-FJ9HU", "Blue")
        self.assertEqual(print_out, "Invalid staff id")

    def test_not_existing_id(self):
        """ This function test for existing id"""
        print_out = self.dojo.rellocate("F-GHJ7Y", "Blue")
        self.assertEqual(print_out, "Fellow id does not exist")
        print_out = self.dojo.rellocate("S-AS23Y", "Blue")
        self.assertEqual(print_out, "Staff id does not exist")

    def test_room_exist(self):
        """ This function test if the room supplied exist"""
        self.dojo.create_room(["Blue"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        print_out = self.dojo.rellocate(new_fellow.ID, "Green")
        self.assertEqual(print_out, "Room does not exist")

    def test_office_to_livingspace(self):
        """ This function test if room rellocating to is of the same type"""
        self.dojo.reset()
        self.dojo.create_room(["Blue"], "office")
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "N")
        print_out = self.dojo.rellocate(new_fellow.ID, "Green")
        self.assertEqual(print_out, \
                    "Cannot move a person from office to livingspace")

    def test_livingspace_to_office(self):
        """ This function test if room rellocating to is of the same type"""
        self.dojo.reset()
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "N")
        self.dojo.create_room(["Blue"], "office")
        print_out = self.dojo.rellocate(new_fellow.ID, "lue")
        self.assertEqual(print_out, \
                    "Cannot move a person from livingspace to office")

    def test_room_full(self):
        self.dojo.reset()
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        new_fellow = self.dojo.add_person("Jeremy Parker", "fellow", "Y")
        new_fellow = self.dojo.add_person("Jeremy Henshaw", "fellow", "Y")
        new_fellow = self.dojo.add_person("Jeremy Crowell", "fellow", "Y")
        self.dojo.create_room(["Blue"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Python", "fellow", "Y")
        print_out = self.dojo.rellocate(new_fellow.ID, "Green")
        self.assertEqual(print_out, \
                    "The livingspace selected is full")
