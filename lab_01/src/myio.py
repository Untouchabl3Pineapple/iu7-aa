import string
import random


def getRandomString(str_len: int) -> str:
    chars = string.ascii_lowercase
    return "".join(random.choice(chars) for i in range(str_len))