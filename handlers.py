import sys
from classes import AddressBook, Record
import validators

def close(args = None, book = None):
    print("Good bye!")
    sys.exit(0)

def help(args = None, book = None):
    return (
        "Available commands:\n"
        "- hello: Greet the user\n"
        "- add <name> <phone>: Add a new contact\n"
        "- change <name> <new_phone>: Change an existing contact's phone\n"
        "- phone <name>: Find a contact by name\n"
        "- all: List all contacts\n"
        "- add-birthday <name> <birthday>: Add a birthday to a contact\n"
        "- show-birthday <name>: Show a contact's birthday\n"
        "- birthdays: List upcoming birthdays\n"
        "- close or exit: Exit the program\n"
    )

@validators.add_contact_validator
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@validators.list_contacts_validator
def list_contacts(args, book: AddressBook):
    return "\n".join(f"{rec}" for rec in book.values())

@validators.find_contact_validator
def find_contact(args, book: AddressBook):
    name = args[0]
    rec = book.find(name)
    return f"{rec}" if rec else "Contact not found."

@validators.change_contact_validator
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    rec = book.find(name)
    if rec is None:
        return "Contact not found."
    
    rec.edit_phone(old_phone, new_phone)
    return "Contact updated."

@validators.add_birthday_validator
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    record.add_birthday(birthday)
    return "Birthday added."

@validators.show_birthday_validator
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    return f"{name}'s birthday is {record.birthday}."

@validators.birthdays_validator
def birthdays(args, book: AddressBook):
    """Повертає список користувачів, яких потрібно привітати по днях на наступному тижні"""
    
    birthdays_list = book.get_upcoming_birthdays()
    
    if not birthdays_list:
        return "No upcoming birthdays."
    
    return "\n".join(f"{record.name}: {record.show_birthday()}" for record in birthdays_list)