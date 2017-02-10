from unittest import TestCase
from rooms.dojo import Dojo
from persons.staffs import Staff
from persons.fellows import Fellow
from persons.persons import Person

class TestPersons(TestCase):
    def test_add_person_successfully(self):
        """ This function test for successful adding of person """
        new_person = Dojo()

        """ This check successful adding of staff person """
        new_staff = new_person.add_person("Andy Carroll", "staff")
        self.assertIsInstance(new_staff, Staff)
        self.assertEqual(new_staff.name, "Andy Carroll")
        self.assertIsInstance(new_staff, Person)

        """ This check successful adding of fellow person """
        new_fellow = new_person.add_person("Jeremy Johnson", "fellow", "Y")
        self.assertIsInstance(new_fellow, Fellow)
        self.assertEqual(new_fellow.name, "Jeremy Johnson")
        self.assertIsInstance(new_fellow, Person)
        self.assertEqual(new_fellow.livingspace, "")

    def test_add_person_invalid_input(self):
        """ This function checks for invalid inputs """
        new_person = Dojo()

        """ Returns error message instead of object staff with invalid inputs """
        new_staff = new_person.add_person("Andy Carroll", "staff", "Y")
        self.assertEqual(new_staff, "Staff cannot request for a livingspace!")
        new_staff = new_person.add_person("  ", "staff")
        self.assertEqual(new_staff, "Person cannot be created with an empty name!")
        new_staff = new_person.add_person("Samora Dake", "type", "Y")
        self.assertEqual(new_staff, "Person cannot be created due to invalid designation!")
