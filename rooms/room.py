from abc import ABCMeta


class Room(metaclass=ABCMeta):
    """ This is the base class for office and livingspace class """

    def __init__(self, name):
        self.name = name
