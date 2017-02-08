#!/usr/bin/env python

import sys
import cmd
from docopt import docopt, DocoptExit


def docopt_cmd(func):
    """
    This decorator
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # It prints a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class TheDojo (cmd.Cmd):
    intro = 'Welcome to The Dojo Office Allocation Program!' \
        + ' (type help for a list of commands.)'
    prompt = 'The_Dojo >>> '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>...  """

        roomType = arg['<room_type>']
        rooms = arg['<room_name>']
        for room in rooms:
            print('An ' + roomType + ' called ' + room + ' has been successfully created')

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> (fellow | staff) [<wants_accommodation>]"""
        fname = arg['<first_name>']
        lname = arg['<last_name>']
        fellow = arg['fellow']
        accd =arg['<wants_accommodation>']
        if fellow:
            print("Fellow " + fname + " " + lname + " has been successfuly added")
        else:
            print("Staff " + fname + " " + lname + " has been successfuly added")
        print(fname + " has been allocated the office Blue")
        if accd == "Y" and fellow:
            print(fname + " has been allocated the livingspace Python")

    def do_quit(self, arg):
        """Exists The Dojo."""

        print('=========== Good Bye =============!\n')
        exit()


TheDojo().cmdloop()

print(opt)
