from unittest import TestCase
from rooms.dojo import Dojo
from persons.staffs import Staff
from persons.fellows import Fellow
from persons.persons import Person
import sys


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

    def test_add_person_invalid_input_1(self):
        """ This function checks for invalid inputs """
        new_staff = self.dojo.add_person("Andy Carroll", "staff", "Y")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Staff cannot request for a livingspace!")

    def test_add_person_invalid_input_2(self):
        new_staff = self.dojo.add_person("  ", "staff")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, \
                    "Person cannot be created with an empty name!")

    def test_add_person_invalid_input_3(self):
        new_staff = self.dojo.add_person("Samora Dake", "type", "Y")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, \
                    "Person cannot be created due to invalid designation!")


class TestReallocate(TestCase):
    dojo = Dojo()
    def test_empty_valid_id(self):
        """ this function test for empty invalid id"""
        self.dojo.reallocate_person(" ", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Invalid id supplied")

    def test_wrong_format_invalid_id(self):
        """ this function test for wrong format invalid id"""
        self.dojo.reallocate_person("asdff", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Invalid id supplied")

    def test_wrong_invalid_id(self):
        """ this function test for wrong invalid id"""
        self.dojo.reallocate_person("A-FG4HU", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Invalid id supplied")

    def test_fellow_not_existing_id(self):
        """ This function test for fellow existing id"""
        self.dojo.reallocate_person("F-GHJ7Y", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "The id supplied is not found")

    def test_staff_not_existing_id(self):
        """ This function test for staff existing id"""
        self.dojo.reallocate_person("S-AS23Y", "Blue")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "The id supplied is not found")

    def test_room_exist(self):
        """ This function test if the room supplied exist"""
        self.dojo.reset()
        self.dojo.create_room(["Blue"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(output[len(output) - 1], "Room not found")


    def test_add_staff_to_livingspace(self):
        """ This function test staff rellocating to livingspace"""
        self.dojo.reset()
        self.dojo.create_room(["Blue"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "staff")
        self.dojo.create_room(["Green"], "livingspace")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(output[len(output) - 1], \
                            "Staff cannot be moved to a livingspace")

    def test_fellow_office_reallocate(self):
        """ This function test if fellow office reallocation is successful"""
        self.dojo.reset()
        self.dojo.create_room(["Green"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "N")
        self.dojo.create_room(["Brown"], "office")
        self.dojo.reallocate_person(new_fellow.ID, "Brown")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(output[len(output) - 1], \
                    "Fellow has been successfully moved to the new office")

    def test_staff_office_reallocate(self):
        """ This function test if staff office reallocation is successful"""
        self.dojo.reset()
        self.dojo.create_room(["Green"], "office")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "staff")
        self.dojo.create_room(["Brown"], "office")
        self.dojo.reallocate_person(new_fellow.ID, "Brown")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(output[len(output) - 1], \
                    "Staff has been successfully moved to the new office")

    def test_fellow_livingspace_reallocate(self):
        """ This function test if fellow room reallocation is successful"""
        self.dojo.reset()
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "Y")
        self.dojo.create_room(["Brown"], "livingspace")
        self.dojo.reallocate_person(new_fellow.ID, "Brown")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(output[len(output) - 1], \
                "Fellow has been successfully moved to the new livingspace")

    def test_fellow_livingspace(self):
        """ This function test if room rellocating to is of the same type"""
        self.dojo.reset()
        self.dojo.create_room(["Green"], "livingspace")
        new_fellow = self.dojo.add_person("Jeremy Johnson", "fellow", "N")
        self.dojo.reallocate_person(new_fellow.ID, "Green")
        output = sys.stdout.getvalue().strip()
        output = output.split("\n")
        self.assertEqual(output[len(output) - 1], \
                    "Fellow does not want a livingspace")

    def test_room_full(self):
        self.dojo.reset()
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
        self.assertEqual(output[len(output) - 1], \
                    "The room selected is full")


class TestLoadPeople(TestCase):
    dojo = Dojo()
    def test_file_exist(self):
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "File not found")

    def test_load_successful(self):
        file_content = "OLUWAFEMI SULE FELLOW Y\n\
                        DOMINIC WALTERS STAFF\n\
                        SIMON PATTERSON FELLOW Y\n\
                        MARI LAWRENCE FELLOW Y\n\
                        LEIGH RILEY STAFF\n\
                        TANA LOPEZ FELLOW Y\n\
                        KELLY McGUIRE STAFF"
        file = open("data/people.txt", "w" )
        file.write(file_content.upper())
        file.close()
        self.dojo.reset()
        self.dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Operation successful")
        self.assertEqual(len(self.dojo.staff_list), 3)
        self.assertEqual(len(self.dojo.fellow_list), 4)
