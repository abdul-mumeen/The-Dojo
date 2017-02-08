from unittest import TestCase
from classes.persons import Persons

class TestPersons(TestCase):
    def test_add_person_successfully(self):
        new_person = Persons()
        added = new_person.add_person("Andy Carroll", "STAFF")
        self.assertTrue(added)
        self.assertEqual(new_person.name,"Andy Carroll")
        second_person = Persons()
        added = second_person.add_person("Jeremy Johnson", "FELLOW",True)
        self.assertTrue(added)
        self.assertEqual(second_person.name,"Jeremy Johnson")
        self.assertTrue(second_person.livingspace)

    def test_add_person_invalid(self):
