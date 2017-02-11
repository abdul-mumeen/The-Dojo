from persons.persons import Person

class Fellow(Person):
    """docstring for Fellow."""
    def __init__(self):
        super(Fellow, self).__init__()
        self.want_office = ""
        self.livingspace = ""
