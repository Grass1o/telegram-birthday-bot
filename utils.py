from datetime import datetime

def validate_birthday(birthday):
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
        return True
    except ValueError:
        return False
