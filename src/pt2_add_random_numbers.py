import random

def add_random_numbers(start=0, end=1000):
    """
    Generates and sums random numbers within a specified range.

    Args:
        start (int, optional): The starting index of the range (default is 0).
        end (int, optional): The ending index of the range (default is 1000).

    Returns:
        int: The sum of randomly generated numbers within the range.
    """
    total_sum = 0
    for _ in range(start, end):
        total_sum += random.randint(1, 1000)
    return total_sum

    total_sum = 0
    for _ in range(start, end):
        total_sum += random.randint(1, 1000)
    return total_sum

