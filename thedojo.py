#!/usr/bin/env python
import cmd
import os

from docopt import docopt, DocoptExit
from termcolor import cprint
from pyfiglet import figlet_format

from rooms.dojo import Dojo
from utils.custom_messages import (
    invalid_command, unexpected_error, welcome_message, missing_command,
    state_overwrite_warning, invalid_wants_accomodation
)


def docopt_cmd(func):
    """ This is the decorator for the functions running the commands """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # It prints a message to the user and the usage block.
            cprint(invalid_command, "yellow")
            cprint(e, "cyan")
            return
        except:
            cprint(unexpected_error, "yellow")

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class TheDojo (cmd.Cmd):
    os.system("clear")
    cprint(figlet_format("The Dojo", font="starwars"),
           "yellow", attrs=["bold"])
    intro = welcome_message
    prompt = "The_Dojo >>> "
    doc_header = "List of commands that can be used in this app"
    dojo = Dojo()

    def default(self, line):
        cprint(missing_command.format(line), "yellow")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
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
        """Usage: add_person <first_name> <last_name> (fellow | staff)""" \
        """ [<wants_accommodation>]"""
        fname = arg['<first_name>']
        lname = arg['<last_name>']
        fellow = arg['fellow']
        designation = "fellow" if fellow else "staff"
        accommodation = arg['<wants_accommodation>']
        if accommodation and accommodation.lower() not in \
                ["y", "yes", "no", "n"]:
            cprint(invalid_wants_accomodation, "red")
            return
        accommodation = "Y" if accommodation and accommodation.lower() in \
            ["y", "yes"] else "N"
        new_person = self.dojo.add_person(fname + " " + lname,
                                          designation, accommodation)
        if new_person:
            new_person.print_creation_info()

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <unique_id> <new_room>"""
        person_id = arg['<unique_id>']
        new_room = arg['<new_room>']
        self.dojo.reallocate_person(person_id, new_room)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""
        self.dojo.load_people(arg['<file_name>'])

    @docopt_cmd
    def do_print_people(self, arg):
        """Usage: print_people (fellow | staff)"""
        fellow = arg['fellow']
        designation = "fellow" if fellow else "staff"
        self.dojo.print_person_list(designation)

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        db_name = arg['--db']
        self.dojo.save_state(db_name)

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        cprint(state_overwrite_warning, "red")
        overwrite = input("(y/n): ")
        if overwrite.lower() == "y":
            self.dojo.load_state(arg['<sqlite_database>'])

    @docopt_cmd
    def do_print_rooms(self, arg):
        """Usage: print_rooms"""
        self.dojo.print_rooms()

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        cprint("=========== Good Bye =============!\n", "green")
        exit()


TheDojo().cmdloop()
