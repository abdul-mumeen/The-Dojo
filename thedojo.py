#!/usr/bin/env python

import sys
import cmd
from docopt import docopt, DocoptExit
from rooms.dojo import Dojo


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

        # except SystemExit:
        #     # The SystemExit exception prints the usage for --help
        #     # We do not need to do the print here.
        #     print("low waist")
        #     return

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
    dojo = Dojo()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>  """
        room = arg['<room_name>']
        self.dojo.print_room(room)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]  """
        file_name = arg['--o']
        self.dojo.print_allocation(file_name)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]  """
        file_name = arg['--o']
        self.dojo.print_unallocated(file_name)

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>...  """

        room_type = arg['<room_type>']
        rooms = arg['<room_name>']
        self.dojo.create_room(rooms, room_type)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> (fellow | staff) \
                                                [<wants_accommodation>]"""
        fname = arg['<first_name>']
        lname = arg['<last_name>']
        fellow = arg['fellow']
        designation = "fellow" if fellow else "staff"
        accommodation =arg['<wants_accommodation>']
        accommodation = "N" if not accommodation else accommodation
        new_person = self.dojo.add_person(fname + " " + lname, \
                                                designation, accommodation)
        if new_person:
            new_person.print_me()

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <unique_id> <new_room>"""
        person_id = arg['<unique_id>']
        new_room = arg['<new_room>']
        self.dojo.reallocate_person(person_id, new_room)

    @docopt_cmd
    def do_quit(self, arg):
        """Exits The Dojo."""
        print('=========== Good Bye =============!\n')
        exit()

TheDojo().cmdloop()
print(opt)
