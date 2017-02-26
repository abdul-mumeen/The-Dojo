class Room(object):
    """ This is the base class for office and livingspace class """

    def __init__(self, name, total_space=4):
        self.name = name
        self.total_space = total_space
