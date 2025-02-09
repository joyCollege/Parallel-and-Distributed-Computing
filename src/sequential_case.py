import time
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def sequential_case(n):
    """
    Executes the operations sequentially and measures the total execution time.

    This function calls the `join_random_letters` and `add_random_numbers` 
    functions in sequence, timing the total execution and printing the time 
    taken in milliseconds.

    Parameters:
    n (int): The number of iterations for each function.

    Returns:
    float: The total time taken in milliseconds for the sequential operations.
    """
    total_start_time = time.time()
    join_random_letters(n)
    add_random_numbers(n)
    total_end_time = time.time()
    
    total_time = (total_end_time - total_start_time) * 1000
    print(f"Serial case taken: {total_time} milliseconds")
    return total_time