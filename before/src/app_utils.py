from random import choices
from string import ascii_letters


def generate_random_id(length: int = 32) -> str:
    return "".join(choices(list(ascii_letters), k=length))
