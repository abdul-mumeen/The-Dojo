from unittest import TestCase
from classes.persons import Persons

class TestPersons(TestCase):
    def test_add_person_successfully(self):
        new_person = Persons()
        added = new_person.add_person("Andy Carroll", "STAFF")
        self.assertTrue(added)
        self.assertEqual(new_person.name,"Andy Carroll")
    #def test_add_person_invalid(self):
