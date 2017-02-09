from unittest import TestCase
from classes.persons import Persons

class TestPersons(TestCase):
    def test_add_person_successfully(self):
        new_person = Persons()
        new_staff = new_person.add_person("Andy Carroll", "staff")
        self.assertIsInstance(Staff)
        self.assertEqual(new_staff.name,"Andy Carroll")
        self.assertIsInstance(Employee)
        new_fellow = new_person.add_person("Jeremy Johnson", "fellow","Y")
        self.assertIsInstance(Fellow)
        self.assertEqual(new_fellow.name,"Jeremy Johnson")
        self.assertIsInstance(Employee)
        self.assertEqual(new_fellow.livingspace,"")

    def test_add_person_invalid_input(self):
        new_person = Persons()
        new_staff = new_person.add_person("Andy Carroll", "staff", "Y")
        self.assertEqual(new_staff,"Staff cannot request for a livingspace!")
        new_staff = new_person.add_person("  ", "staff")
        self.assertEqual(new_staff,"Staff cannot be created with empty name!")
        new_staff = new_person.add_person("Samora Dake","type","Y")
        self.assertEqual(new_staff,"Person cannot br created due to invalid designation!")
