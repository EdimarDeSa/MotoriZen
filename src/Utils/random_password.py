import random
import string


def generate_random_password(digits: int = 8) -> str:
    password_charset: list[str] = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ] + random.choices(string.ascii_letters + string.digits + string.punctuation, k=digits - 4)

    random.shuffle(password_charset)

    password = "".join(password_charset)

    return password
