import random
import string


def join_random_letters(n=1000 ):
    """
    Generates a random string of letters.

    This function creates a string by randomly selecting `n` letters 
    (both uppercase and lowercase) from the English alphabet.

    Parameters:
    n (int, optional): The length of the generated string. Default is 1000.

    Returns:
    str: A string containing `n` randomly selected letters.
    """
    letters = [random.choice(string.ascii_letters) for _ in range(n)]
    joined_letters = ''.join(letters)
    return joined_letters