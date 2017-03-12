import random
import string

from termcolor import cprint


class Person(object):

    """This is the base class for staff and fellow"""

    def __init__(self, name, designation):
        self.name = name
        self.ID = None
        self.office = None
        self.designation = designation
        self.existing_ids = []

    def get_existing_id(self, person_list):
        """This function extracts a list of existing id from person list"""
        return [person.ID for person in person_list]

    def generate_id(self, person_list):
        """This function generates id for either staff or fellow."""
        prefix = '{}-'.format(self.designation[0].upper())
        id_exist = True
        person_id = ""
        while id_exist:
            person_id = prefix + ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(5)
            )
            if person_id not in self.get_existing_id(person_list):
                id_exist = False
                self.ID = person_id

    def print_creation_info(self):
        first_name = self.name.split()[0].title()
        cprint("{} {} has been successfully added with ID {}.".format(
            self.designation.title(), self.name.title(), self.ID.upper()),
            "green")
        if self.office:
            cprint("{} has been allocated the office {}".format(
                first_name, self.office.name.title()), "green")
        else:
            cprint("{} has been placed".format(first_name) +
                   " on a waiting list for office", "yellow")
