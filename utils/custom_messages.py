invalid_command = (
    'Invalid Command: the value(s) are not entered' +
    'correctly!\nKindly check the usage bellow'
)

unexpected_error = "The operation failed due to unexpected error!"
welcome_message = (
    "\t\tWelcome to The Dojo Office Allocation Program!\n"
    "\t\t\t(type help for a list of commands.)\n"
)
missing_command = "There is no command such as '{}'"
invalid_wants_accomodation = (
    "Invalid option for accommodation, availble options are;"
    " Y, N, Yes and No"
)
state_overwrite_warning = (
    "Loading a state will overwrite the current state!\n"
    "Do you want to continue"
)
empty_room_name_error = (
    "The {} at index {} cannot be created due to empty room name."
)
invalid_room_name_error = "Invalid {} name '{}' supplied!"
room_exist_error = "The {} name '{}' already existed."
invalid_room_type_error = "Cannot create room(s), invalid room type enterred"
empty_room_type_and_name_error = (
    "Cannot create rooms with empty room name and/or empty room type"
)
office_created = "An office called {} has been successfully created"
livingspace_created = "A livingspace called {} has been successfully created"
livingspace_request_error = "Staff cannot request for a livingspace!"
invalid_designation_error = (
    "Person cannot be created due to invalid designation!"
)
empty_allocation_list = "Nobody on the allocated list."
empty_room_list = "No room added yet"
empty_unallocated_list = "Nobody on the unallocated list."
file_exist_error = "A file with the name supplied already exist."
file_operation_menu = "Press a - to append, w - to overwrite, c - to cancel"
empty_file_name_info = "List not written to file, no file name supplied"
file_cancelled_message = "Write to file cancelled"
write_to_file_success = "List have been successfully {} to file '{}.txt'"
room_full_error = "The room selected is full"
missing_id_error = "The id supplied is not found"
invalid_id = "Invalid id supplied"
staff_livingspace_error = "Staff cannot be moved to a livingspace"
same_livingspace_error = "Fellow is currently assigned to this livingspace"
livingspace_not_request = "Fellow does not want a livingspace"
fellow_reallocate_livingspace = (
    "Fellow has been successfully reallocated to livingspace "
)
same_office_error = "{} is currently assigned to this office"
office_reallocate_success = "{} has been successfully reallocated to office "
empty_person_list = "This list is empty, no one has been added yet"
line_not_loaded_error = "line {} was not loaded because of the above^^ reason"
line_parameter_error = (
    "line {} was not loaded because of invalid parameters supplied"
)
people_loaded_info = "{} on the list have been successfully loaded"
empty_file_error = "The file selected is empty"
state_loaded_info = "Data in {}.sqlite have been successfully loaded"
