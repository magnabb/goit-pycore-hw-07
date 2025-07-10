from ast import Dict
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits long and contain only digits. Got: " + value)
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
        try:
            if not isinstance(value, str):
                raise ValueError("Birthday must be a string in the format DD.MM.YYYY")
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.birthday: Birthday | None = None
        self.phones = []
    
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break
    
    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def show_birthday(self) -> str:
        if self.birthday is None:
            return "Birthday not set"
        return self.birthday.value.strftime("%d.%m.%Y")


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    data: dict[str, Record] 
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Record | None:
        return self.data.get(name)
    
    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self, upcoming_days: int = 7, today: datetime = datetime.now()) -> list[Record]:
        if not isinstance(today, datetime):
            raise ValueError("Today must be a datetime object got: " + type(today))
        if not isinstance(upcoming_days, int) or upcoming_days < 0:
            raise ValueError("Upcoming days must be a non-negative integer. Got: " + str(upcoming_days))

        if len(self.data) == 0:
            return []

        upcoming_date = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=upcoming_days)

        return [rec for rec in self.data.values() if rec.birthday is not None and 0 <= (upcoming_date.date() - rec.birthday.value).days <= 7]