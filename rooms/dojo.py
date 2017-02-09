class Dojo(object):
    def __init__(self):
        self.all_rooms = []

    def create_room(self, room_name, room_type):
        log = ""
        if room_type.strip() != "" and len(room_name) > 0:
            if room_type == "office":
                for i in range(0,len(room_name)):
                    if room_name[i].strip() == "":
                        log += "\nThe office at index " + str(i) + " cannot be created due to empty name."
                    elif nameExist(room_name[i]):
                        log += "\nThe name of office " + str(i) + " already existed."
                    else:
                        new_office = Office(room_name[i],6)
                        self.all_rooms.append(new_office)
            elif room_type == "livingspace":
                for i in range(0,len(room_name)):
                    if room_name[i].strip() == "":
                        log += "\nThe livingspace at index " + str(i) + \
                        " cannot be created due to empty name."
                    elif nameExist(room_name[i]):
                        log += "\nThe name of livingspace " + str(i) + " already existed."
                    else:
                        new_office = Livingspace(room_name[i],4)
                        self.all_rooms.append(new_office)
            else:
                log += "\nCannot creae room(s), invalid room type enterred"
        else:
            log += "Cannot create rooms with empty room name and/or empty room type"
        if log == "":
            return True
        else:
            return log
