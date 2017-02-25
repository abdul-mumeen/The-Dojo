import os
from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace

class DB(object):
    def __init__(self):
        pass

    def save_state(self, db_name, room_list, person_list):
        if db_name.strip() == "":
            db_name = self.generate_name():
        if self.db_exist(db_name):
            return "Database name already existed!\
                                    \nKindly choose another name."
        else:
            sqlite_file = "data/{}.sqlite".format(db_name)
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("CREATE TABLE room_table (name TEXT PRIMARY KEY, \
                                            type TEXT, capacity INTEGER)")


            c.execute("CREATE TABLE person_table (id TEXT PRIMARY KEY,\
                                name TEXT, designation TEXT, office TEXT)")

            c.execute("CREATE TABLE livingspace_table (id TEXT PRIMARY KEY,\
                                wants_accommodation TEXT, livingspace TEXT)")


            for person in person_list:
                office = person.office.name if person.office is not None \
                                                                    else ""
                c.execute("INSERT INTO person_table (id, name, designation, \
                        office) VALUES ({}, {}, {}, {})".format(person.ID, \
                                    person.name, person.designation, office))
                if person.designation.lower() == "fellow":
                    LivingSpace = person.livingspace.name if \
                                    person.livingspace is not None else ""
                    c.execute("INSERT INTO livingspace_table (id, \
                            wants_accommodation, livingspace) VALUES \
                                ({}, {}, {})".format(person.ID, \
                                    person.wants_accommodation, LivingSpace))

            conn.commit()
            conn.close()

    def insert_rooms(self, room_list):
        for room in room_list:
            try:
                room_type = "office" if isinstance(room, Office) \
                                                        else "livingspace"
                c.execute("INSERT INTO room_table (name, type, capacity) \
                                    VALUES ({}, {}, {})".format(room.name,\
                                                room_type, room.total_space))
            except sqlite3.IntegrityError:
                print('ERROR: failed to insert room {}'.format(room.name))
