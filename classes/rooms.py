class Rooms(object):
    def __init__(self):
        self.name 
    def create_room(self, room_type, room_name):
        if room_type != "" and room_name != "":
            self.room_type = room_type
            self.room_name = room_name
            self.all_rooms.append(room_name)
            return True
