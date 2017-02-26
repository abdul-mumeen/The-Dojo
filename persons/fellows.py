from persons.persons import Person

class Fellow(Person):
    """ This is a fellow class. It inherits from the person class"""
    
    def __init__(self, name, designation):
        super().__init__(name, designation)
        self.wants_accommodation = False
        self.livingspace = None

    def print_me(self):
        first_name = self.name.split()[0].title()
        super().print_me()
        if self.livingspace:
            print("{} has been allocated ".format(first_name) + \
                        "the livingspace {}".format(\
                            self.livingspace.name.title()))
        else:
            if self.wants_accommodation:
                print("{} has been placed".format(first_name) + \
                            " on a waiting list for livingspace")
