from functools import wraps

from classes import AddressBook, Record

def change_contact_validator(func):
    @wraps(func)
    def wrapper(args, contacts):
        if len(args) != 3:
            return "Invalid number of arguments. Usage: change <name> <old_phone> <new_phone>"
        return func(args, contacts)
    return wrapper

def find_contact_validator(func):
    @wraps(func)
    def wrapper(args, contacts):
        if len(args) != 1:
            return "Invalid number of arguments. Usage: find <name>"
        return func(args, contacts)
    return wrapper

def list_contacts_validator(func):
    @wraps(func)
    def wrapper(args, book: AddressBook):
        if not isinstance(book, AddressBook) or not book.data:
            return "No contacts found."
        return func(args, book)
    return wrapper

def add_contact_validator(func):
    @wraps(func)
    def wrapper(args, contacts):
        if len(args) != 2:
            return "Invalid number of arguments. Usage: add <name> <phone>"
        name, phone = args
        if not name or not phone:
            return "Name and phone cannot be empty."
        return func(args, contacts)
    return wrapper

def parse_input_validator(func):
    @wraps(func)
    def wrapper(user_input):
        if not user_input:
            return "Invalid input. Please enter a command."
        return func(user_input)
    return wrapper

def add_birthday_validator(func):
    @wraps(func)
    def wrapper(args, book: AddressBook):
        if len(args) != 2:
            return "Invalid number of arguments. Usage: add_birthday <name> <birthday>"
        if not isinstance(book, AddressBook):
            return "Invalid address book instance."
        
        name, birthday = args
        if not name or not birthday:
            return "Name and birthday cannot be empty."
        
        r = Record('')
        try:
            r.add_birthday(birthday)
        except ValueError as e:
            return str(e)
        
        return func(args, book)
    return wrapper

def show_birthday_validator(func):
    @wraps(func)
    def wrapper(args, book: AddressBook):
        if len(args) != 1:
            return "Invalid number of arguments. Usage: show_birthday <name>"
        if not isinstance(book, AddressBook):
            return "Invalid address book instance."
        name = args[0]
        if not name:
            return "Name cannot be empty."
        return func(args, book)
    return wrapper

def birthdays_validator(func):
    @wraps(func)
    def wrapper(args, book: AddressBook):
        if not isinstance(book, AddressBook):
            return "Invalid address book instance."
        return func(args, book)
    return wrapper
