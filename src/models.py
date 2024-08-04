import re
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if self.validate_phone(value):
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits.")

    @staticmethod
    def validate_phone(value: str) -> bool:
        return bool(re.fullmatch(r'\d{10}', value))

class Birthday(Field):
    def __init__(self, value: str):
        if self.validate_birthday(value):
            super().__init__(value)
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @staticmethod
    def validate_birthday(value: str) -> bool:
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                break

    def find_phone(self, phone: str) -> Phone:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = ', '.join(phone.value for phone in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday = bday.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                days_until_birthday = (bday - today).days
                if 0 <= days_until_birthday <= 7:
                    if bday.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
                        days_to_monday = 7 - bday.weekday()
                        congratulation_date = bday + timedelta(days=days_to_monday)
                    else:
                        congratulation_date = bday
                    upcoming.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return upcoming
