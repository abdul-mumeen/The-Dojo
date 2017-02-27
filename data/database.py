import os
import datetime
import sqlite3

from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace


class DB(object):
    def save_state(self, db_name, room_list, person_list):
        if db_name.strip() == "":
            db_name = self.generate_name()
        if self.db_exist(db_name):
            return "Database name already existed!" + \
                                    " Kindly choose another name."
        else:
            sqlite_file = "data/{}.sqlite".format(db_name)
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            self.run_migrations(c)
            self.insert_rooms(room_list, c)
            self.insert_people(person_list, c)
            conn.commit()
            conn.close()
            return "The state has been successfully saved with %s.sqlite" \
                   % db_name

    def insert_rooms(self, room_list, c):
        for room in room_list:
            try:
                room_type = "office" if isinstance(room, Office) \
                                                        else "livingspace"
                c.execute("INSERT INTO room_table (name, type, capacity) \
                          VALUES ('{}', '{}', '{}')".format(
                                room.name, room_type, room.total_space))
            except sqlite3.IntegrityError:
                print('ERROR: failed to insert room {}'.format(room.name))

    def insert_people(self, person_list, c):
        for person in person_list:
            office = person.office.name if person.office is not None else ""
            c.execute(
                "INSERT INTO person_table (id, name, designation, " +
                "office) VALUES ('{}', '{}', '{}', '{}')".format(
                    person.ID, person.name, person.designation, office))
            if person.designation.lower() == "fellow":
                livingSpace = person.livingspace.name if \
                                person.livingspace is not None else ""
                c.execute("INSERT INTO livingspace_table (ids, \
                        wants_accommodation, livingspace) VALUES \
                            ('{}', '{}', '{}')".format(
                            person.ID,
                            person.wants_accommodation, livingSpace))

    def db_exist(self, db_name):
        if os.path.isfile("data/{}.sqlite".format(db_name)):
            return True
        else:
            return False

    def generate_name(self):
        i = datetime.datetime.now()
        db_name = str(i.year) + str(i.month) + str(i.day) + str(i.hour) \
            + str(i.minute) + str(i.second)
        while self.db_exist(db_name):
            db_name = str(int(db_name) + 1)
        return db_name

    def run_migrations(self, c):
        c.execute("CREATE TABLE room_table (name TEXT PRIMARY KEY, \
                                        type TEXT, capacity INTEGER)")

        c.execute("CREATE TABLE person_table (id TEXT PRIMARY KEY,\
                            name TEXT, designation TEXT, office TEXT)")

        c.execute("CREATE TABLE livingspace_table (ids TEXT PRIMARY KEY,\
                            wants_accommodation TEXT, livingspace TEXT)")

    def load_state(self, db_name):
        sqlite_file = "data/{}.sqlite".format(db_name)
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("select name, type from room_table")
        db_room_list = c.fetchall()

        room_list = {}
        for row in db_room_list:
            new_room = Office(row[0]) if row[1].lower() == \
                    "office" else LivingSpace(row[0])
            room_list[new_room.name] = new_room

        fellow_list = []
        c.execute("select id, name, designation, office," +
                  " wants_accommodation, livingspace from " +
                  "person_table INNER JOIN " +
                  "livingspace_table ON id = " +
                  "ids WHERE designation = 'fellow'")
        db_fellow_list = c.fetchall()
        for row in db_fellow_list:
            new_fellow = Fellow(row[1], row[2])
            new_fellow.ID = row[0]
            new_fellow.office = room_list[row[3]] if row[3] \
                and row[3] in room_list else None
            new_fellow.wants_accommodation = row[4]
            new_fellow.livingspace = room_list[row[5]] \
                if row[5] and row[5] in room_list else None
            fellow_list.append(new_fellow)
            
        staff_list = []
        c.execute(
            "select id, name, designation, office" +
            " from person_table WHERE designation = 'staff'")
        db_staff_list = c.fetchall()
        for row in db_staff_list:
            new_staff = Staff(row[1], row[2])
            new_staff.ID = row[0]
            new_staff.office = room_list[row[3]] if row[3] \
                and row[3] in room_list else None
            staff_list.append(new_staff)

        app_data = {"all_rooms": room_list, "staff_list": staff_list,
                    "fellow_list": fellow_list}
        conn.commit()
        conn.close()
        return app_data
