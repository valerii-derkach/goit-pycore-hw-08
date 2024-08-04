from decorators import input_error
from models import AddressBook, Record, Phone, Birthday
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    name, phone = args[0], args[1]
    if not Phone.validate_phone(phone):
        raise ValueError("Phone number must be 10 digits.")
    
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated."
    else:
        return "No such name in contacts."

@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    return "No such name in contacts."

def show_all(book: AddressBook) -> str:
    result = "\n".join(str(record) for record in book.values())
    return result

def show_help() -> str:
    return """
        Available commands:\n
        hello - Display a greeting message.\n
        add username phone - Add a new contact with the specified phone number.\n
        change username old_phone new_phone - Change the phone number for an existing contact.\n
        phone username - Display the phone number for the specified contact.\n
        all - Display all saved contacts with their phone numbers.\n
        add-birthday username birthday - Add a birthday for the specified contact in DD.MM.YYYY format.\n
        show-birthday username - Show the birthday for the specified contact.\n
        birthdays - Show upcoming birthdays in the next week.\n
        close, exit - Exit the bot with a goodbye message.\n
        help - Display this help message.
        """

@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:    
    name, birthday = args[0], args[1]
    if not Birthday.validate_birthday(birthday):
        raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Added birthday for {name}."
    else:
        return "No such name in contacts."

@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value}."
    elif record:
        return f"{name} does not have a birthday set."
    else:
        return "No such name in contacts."

@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    return "\n".join(f"{record['name']} has a birthday on {record['congratulation_date']}" for record in upcoming_birthdays)
