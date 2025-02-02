import random
import string


def join_random_letters():
    letters = [random.choice(string.ascii_letters) for _ in range(1000000)]
    joined_letters = ''.join(letters)
    return joined_letters