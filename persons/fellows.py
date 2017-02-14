from persons.persons import Person


class Fellow(Person):
    """docstring for Fellow."""
    def __init__(self):
        super().__init__()
        self.wants_accommodation = False
        self.livingspace = ""
