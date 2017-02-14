from persons.persons import Person

class Fellow(Person):
    """ This is a fellow class. It inherits from the person class"""
    def __init__(self):
        super().__init__()
        self.wants_accommodation = False
        self.livingspace = ""
