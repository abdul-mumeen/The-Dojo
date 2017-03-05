import os
import datetime
import sqlite3

from persons.staffs import Staff
from persons.fellows import Fellow
from rooms.office import Office
from rooms.livingspace import LivingSpace


class DB(object):
    room_type_mapping = {Office: "office", LivingSpace: "livingspace"}

    def save_state(self, db_name, rooms, person_list):
        """
        This function saves the state of the application by saving data
        such as room collection, staff list and fellow list currently available
        in the application
        """
        if not db_name.strip():
            db_name = self.generate_name()
        if self.db_exists(db_name):
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
            return "The state has been successfully saved in %s.sqlite" \
                   % db_name

    def insert_rooms(self, rooms, c):
        """
        This function executes the sql command insert to
        save each room in the Database
        """
        for room in rooms:
            try:
                room_type = self.room_type_mapping[type(room)]
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
            office = person.office.name if person.office else ""
            c.execute(
                "INSERT INTO person_table (id, name, designation, " +
                "office) VALUES ('{}', '{}', '{}', '{}')".format(
                    person.ID, person.name, person.designation, office))
            if person.designation.lower() == "fellow":
                livingSpace = person.livingspace.name if \
                                person.livingspace else ""
                c.execute("INSERT INTO livingspace_table (ids, \
                        wants_accommodation, livingspace) VALUES \
                            ('{}', '{}', '{}')".format(
                            person.ID,
                            person.wants_accommodation, livingSpace))

    def db_exists(self, db_name):
        """This function check if a database file exist"""
        return os.path.isfile("data/{}.sqlite".format(db_name))

    def generate_name(self):
        """
        This function generates a database name from concatenating
        the year, month, day, hour, minute and second of the moment
        """
        date_time = datetime.datetime.now()
        db_name = "".join([str(date_time.year), str(date_time.month),
                           str(date_time.day), str(date_time.hour),
                           str(date_time.minute), str(date_time.second)])
        while self.db_exists(db_name):
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
        staff_list = self.get_staff_from_db_staff(db_staff_list, rooms)
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
        rooms = []
        rooms_mapping = {"office": Office, "livingspace": LivingSpace}
        for row in db_rooms:
            new_room = rooms_mapping[row[1].lower()](row[0])
            rooms.append(new_room)
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
            new_fellow.office = [
                room for room in rooms
                if room.name.title() == row[3].title()][0] if row[3] and \
                row[3].title() in [room.name.title() for room in rooms] \
                else None
            new_fellow.wants_accommodation = row[4]
            new_fellow.livingspace = [
                room for room in rooms
                if room.name.title() == row[5].title()][0] if row[5] else None
            fellow_list.append(new_fellow)
        return fellow_list

    def get_staff_from_db_staff(self, db_staff_list, rooms):
        """
        This function extracts the collection of rooms from the
        rows of room returned from the database
        """
        staff_list = []
        for row in db_staff_list:
            new_staff = Staff(row[1], row[2])
            new_staff.ID = row[0]
            new_staff.office = [
                room for room in rooms
                if room.name.title() == row[3].title()][0] if row[3] and \
                row[3].title() in [room.name.title() for room in rooms] \
                else None
            staff_list.append(new_staff)
        return staff_list
