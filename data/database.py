import os
import datetime
import sqlite3

from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace


class DB(object):
    def save_state(self, db_name, rooms, person_list):
        """
        This function save the state of the application by saving data
        such as room collection, staff list and fellow list currently used
        in the application
        """
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
            self.insert_rooms(rooms, c)
            self.insert_people(person_list, c)
            conn.commit()
            conn.close()
            return "The state has been successfully saved with %s.sqlite" \
                   % db_name

    def insert_rooms(self, rooms, c):
        """
        This function executes the sql command insert to
        save each room in the Database
        """
        for room in rooms:
            try:
                room_type = "office" if isinstance(room, Office) \
                                                        else "livingspace"
                c.execute("INSERT INTO room_table (name, type, capacity) \
                          VALUES ('{}', '{}', '{}')".format(
                                room.name, room_type, room.total_space))
            except sqlite3.IntegrityError:
                print('ERROR: failed to insert room {}'.format(room.name))

    def insert_people(self, person_list, c):
        """
        This function executes the sql command insert to
        save each person in the Database
        """
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
        """This function check if a database file exist"""
        return True if os.path.isfile("data/{}.sqlite".format(db_name)) \
            else False

    def generate_name(self):
        """
        This function generate a database name from concatenating
        the year, month, day, hour, minute and second of the moment
        """
        i = datetime.datetime.now()
        db_name = str(i.year) + str(i.month) + str(i.day) + str(i.hour) \
            + str(i.minute) + str(i.second)
        while self.db_exist(db_name):
            db_name = str(int(db_name) + 1)
        return db_name

    def run_migrations(self, c):
        """This function creates table for room, person and livingspace"""
        c.execute("CREATE TABLE room_table (name TEXT PRIMARY KEY, \
                                        type TEXT, capacity INTEGER)")

        c.execute("CREATE TABLE person_table (id TEXT PRIMARY KEY,\
                            name TEXT, designation TEXT, office TEXT)")

        c.execute("CREATE TABLE livingspace_table (ids TEXT PRIMARY KEY,\
                            wants_accommodation TEXT, livingspace TEXT)")

    def load_state(self, db_name):
        """
        This function loads application data from the database
        and returns it to the application
        """
        sqlite_file = "data/{}.sqlite".format(db_name)
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute("select name, type from room_table")
        db_rooms = c.fetchall()
        rooms = self.get_rooms_from_db_rooms(db_rooms)

        c.execute("select id, name, designation, office," +
                  " wants_accommodation, livingspace from " +
                  "person_table INNER JOIN " +
                  "livingspace_table ON id = " +
                  "ids WHERE designation = 'fellow'")
        db_fellow_list = c.fetchall()
        fellow_list = self.get_fellows_from_db_fellows(db_fellow_list, rooms)

        c.execute(
            "select id, name, designation, office" +
            " from person_table WHERE designation = 'staff'")
        db_staff_list = c.fetchall()
        staff_list = self.get_staffs_from_db_staffs(db_staff_list, rooms)

        app_data = {"all_rooms": rooms, "staff_list": staff_list,
                    "fellow_list": fellow_list}
        conn.commit()
        conn.close()
        return app_data

    def get_rooms_from_db_rooms(self, db_rooms):
        """
        This function extracts the collection of rooms from the
        rows of room returned from the database
        """
        rooms = {}
        for row in db_rooms:
            new_room = Office(row[0]) if row[1].lower() == \
                    "office" else LivingSpace(row[0])
            rooms[new_room.name] = new_room
        return rooms

    def get_fellows_from_db_fellows(self, db_fellow_list, rooms):
        """
        This function extracts the collection of rooms from the
        rows of room returned from the database
        """
        fellow_list = []
        for row in db_fellow_list:
            new_fellow = Fellow(row[1], row[2])
            new_fellow.ID = row[0]
            new_fellow.office = rooms[row[3]] if row[3] \
                and row[3] in rooms else None
            new_fellow.wants_accommodation = row[4]
            new_fellow.livingspace = rooms[row[5]] \
                if row[5] and row[5] in rooms else None
            fellow_list.append(new_fellow)
        return fellow_list

    def get_staffs_from_db_staffs(self, db_staff_list, rooms):
        """
        This function extracts the collection of rooms from the
        rows of room returned from the database
        """
        staff_list = []
        for row in db_staff_list:
            new_staff = Staff(row[1], row[2])
            new_staff.ID = row[0]
            new_staff.office = rooms[row[3]] if row[3] \
                and row[3] in rooms else None
            staff_list.append(new_staff)
        return staff_list
