import random
import string


def join_random_letters(n=1000 ):
    letters = [random.choice(string.ascii_letters) for _ in range(n)]
    joined_letters = ''.join(letters)
    return joined_letters