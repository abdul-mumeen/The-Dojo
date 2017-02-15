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
        self.assertEqual(new_staff, "Person cannot be created with an empty name!")
        new_staff = self.dojo.add_person("Samora Dake", "type", "Y")
        self.assertEqual(new_staff, "Person cannot be created due to invalid designation!")
