import random
import string
class Person(object):
    """This is the base class for staff and fellow"""
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.office = ""
        self.designation = ""

    def get_existing_id(self, person_list):
        """This function extracts a list of existing id for a list of person"""
        id_list = []
        for i in range(0, len(person_list)):
            id_list.append(person_list[i].ID)
        return id_list

    def generate_id(self, designation, person_list):
        """This function generates id for either staff or fellow."""
        if designation.lower == "fellow":
            id_exist = true
            fellow_id + ""
            while id_exist:
                fellow_id = "F-" + ''.join(\
                        random.choice(string.ascii_uppercase + string.digits)
                                      for _ in range(5))
                if not (fellow_id in self.get_existing_id(person_list)):
                    id_exist = False
            return fellow_id
        else:
            id_exist = True
            staff_id = ""
            while id_exist:
                staff_id = "S-" + ''.join(
                        random.choice(string.ascii_uppercase + string.digits)
                                      for _ in range(5))
                if not (staff_id in self.get_existing_id(person_list)):
                    id_exist = False
            return staff_id
