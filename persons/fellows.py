from termcolor import cprint

from persons.persons import Person


class Fellow(Person):
    """ This is a fellow class. It inherits from the person class"""

    def __init__(self, name):
        super().__init__(name, "fellow")
        self.wants_accommodation = 0
        self.livingspace = None

    def print_creation_info(self):
        first_name = self.name.split()[0].title()
        super().print_creation_info()
        if self.livingspace:
            cprint("{} has been allocated ".format(first_name) +
                   "the livingspace {}".format(
                   self.livingspace.name.title()), "green")
        elif self.wants_accommodation:
            cprint("{} has been placed".format(first_name) +
                   " on a waiting list for livingspace", "yellow")
