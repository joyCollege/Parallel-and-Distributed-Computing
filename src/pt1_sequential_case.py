import time
from .pt2_add_random_numbers import add_random_numbers

def sequential_case(num_numbers=1000):
    """
    Executes a sequential summation of random numbers.

    Args:
        num_numbers (int, optional): The total count of numbers to sum (default is 1000).

    Returns:
        float: The total execution time in milliseconds.

    The function calculates the sum of `num_numbers` random integers sequentially.
    It records the start and end time to measure execution duration.
    """

    print(f"\nStarting the sequential case...")

    total_start_time = time.time()
    result = add_random_numbers(0, num_numbers)
    print(f">> Sum of random numbers: {result}")
    total_end_time = time.time()
    
    total_time = (total_end_time - total_start_time) * 1000
    print(f">> Time taken: {total_time} milliseconds")
    return total_time