import random

def add_random_numbers(n=1000):
    """
    Generates a list of random numbers and calculates their sum.

    This function creates a list of `n` random integers between 1 and 1000 
    and computes their total sum.

    Parameters:
    n (int, optional): The number of random numbers to generate. Default is 1000.

    Returns:
    int: The sum of the generated random numbers.
    """
    numbers = [random.randint(1, 1000) for _ in range(n)]
    total_sum = sum(numbers)
    return total_sum