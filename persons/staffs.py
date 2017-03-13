from persons.persons import Person


class Staff(Person):
    """ This is a staff class. It inherits from the person class"""

    def __init__(self, name):
        super().__init__(name, "staff")
