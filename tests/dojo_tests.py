from unittest import TestCase
from classes.dojo import Dojo

class TestCreatRoom(TestCase):
    def test_create_room_successfully(self):
        ndojo = Dojo()
        initial_room_count = len(ndojo.all_rooms)
        self.assertEqual(initial_room_count,0)
        blue_office = ndojo.create_room("Blue","office")
        self.assertTrue(blue_office)
        new_room_count = len(ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count,1)

    def test_create_multiple_rooms_successfully(self):
        ndojo = Dojo()
        initial_room_count = len(ndojo.all_rooms)
        ndojo.create_room(["Blue", "Green", "Purple"], "office")
        new_room_count = len(ndojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count,3)
        ndojo.create_room(["Yellow", "Brown", "Black"], "livingspace")
        latest_room_count = len(ndojo.all_rooms)
        self.assertEqual(latest_room_count - new_room_count,3)
