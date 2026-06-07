import re

def validate_email(email):
    if '@' in email and '.' in email:
        return True, "Valid email"
    return False, "Invalid email! Use: name@example.com"

def validate_phone(phone):
    numbers = re.sub(r'\D', '', phone)
    if len(numbers) >= 10:
        return True, "Valid phone"
    return False, "Invalid phone! Use at least 10 digits"

def validate_name(name):
    if name and len(name.strip()) >= 2:
        return True, "Valid name"
    return False, "Name is required (min 2 characters)"

def validate_year(year):
    if not year:
        return True, "Optional"
    if year.isdigit() and 1950 <= int(year) <= 2030:
        return True, "Valid year"
    return False, "Invalid year! Use 4 digits (e.g., 2024)"