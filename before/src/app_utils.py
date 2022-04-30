from string import ascii_letters
from random import choices


def generate_random_id(length: int = 32) -> str:
    return "".join(choices(list(ascii_letters), k=length))

