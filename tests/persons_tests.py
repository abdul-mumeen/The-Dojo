from unittest import TestCase
from rooms.dojo import Dojo
from persons.staffs import Staff
from persons.fellows import Fellow
from persons.persons import Person
import sys


class TestPersonClass(TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.new_staff = self.dojo.add_person("Andy Carroll", "staff")
        self.new_staff_2 = self.dojo.add_person("Andy Caroline", "staff")
        self.new_fellow = self.dojo.add_person("Andy Carroll", "fellow")

    def tearDown(self):
        self.dojo.reset()

    def test_get_existing_id(self):
        """ This function test the function that returns existing person id """
        new_person = Person("Usman Benelli", Fellow)
        staff_ids = new_person.get_existing_id(self.dojo.staff_list)
        self.assertEqual(len(staff_ids), 2)
        self.assertEqual(self.new_staff.ID in staff_ids, True)
        fellow_ids = new_person.get_existing_id(self.dojo.fellow_list)
        self.assertEqual(len(fellow_ids), 1)
        self.assertEqual(self.new_fellow.ID in fellow_ids, True)

    def test_generate_id_fellow(self):
        """ This function test for successful generation of fellow id """
        new_fellow = Person("Garba Oluwatomi", "fellow")
        new_fellow.generate_id(self.dojo.fellow_list)
        self.assertEqual(len(new_fellow.ID), 7)
        self.assertEqual(new_fellow.ID[0], "F")
        self.assertNotEqual(new_fellow.ID, self.new_fellow.ID)

    def test_generate_id_fellow(self):
        """ This function test for successful generation of staff id """
        new_staff = Person("Chigozie Oluwatomi", "staff")
        new_staff.generate_id(self.dojo.staff_list)
        self.assertEqual(len(new_staff.ID), 7)
        self.assertEqual(new_staff.ID[0], "S")
        self.assertNotEqual(new_staff.ID, self.new_staff.ID)
        self.assertNotEqual(new_staff.ID, self.new_staff_2.ID)
