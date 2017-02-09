from unittest import TestCase
from classes.dojo import Dojo

class TestCreatRoom(TestCase):
    def test_create_room_successfully(self):
        ndojo = Dojo()
        initial_room_count = len(ndojo.all_rooms)
        self.assertEqual(initial_room_count,0)
        blue_office = ndojo.create_room(["Blue"],"office")
        self.assertTrue(blue_office)
        new_room_count = len(ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count,1)

    def test_create_multiple_rooms_successfully(self):
        ndojo = Dojo()
        initial_room_count = len(ndojo.all_rooms)
        log = ndojo.create_room(["Blue", "Green", "Purple"], "office")
        self.assertTrue(log)
        new_room_count = len(ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count,3)
        ndojo.create_room(["Yellow", "Brown", "Black"], "livingspace")
        latest_room_count = len(ndojo.all_rooms)
        self.assertEqual(latest_room_count - new_room_count,3)
    def test_check_invalid_input(self):
        ndojo = Dojo()
        log = ndojo.create_room([],"  ")
        self.assertEqual(log,"Cannot create rooms with empty room name and/or empty room type")
        log = ndojo.create_room([" "],"office")
        self.assertEqual(log,"\nThe office at index 0 cannot be created due to empty name.")
        log = ndojo.create_room(["Green", " ", "Black"],"livingspace")
        self.assertEqual(log,"\nThe livingspace at index 1 cannot be created due to empty name.")
        log = ndojo.create_room(["Green", "Black"],"piper")
        self.assertEqual(log,"\nCannot creae room(s), invalid room type enterred")
    def test_check_duplicate_names(self):
        ndojo = Dojo()
        log = ndojo.create_room(["Green", "Blue"],"office")
        log = ndojo.create_room(["Blue"],"office")
        self.assertEqual(log,"\nThe name of office at index 0 already existed.")
        log = ndojo.create_room(["Brown","Black","Black"],"livingspace")
        self.assertEqual(log,"\nThe name of office at index 2 already existed.")
