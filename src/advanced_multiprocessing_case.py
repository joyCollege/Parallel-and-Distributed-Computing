import time
import multiprocessing
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def advanced_multiprocessing_case(n):
    """
    Executes tasks in parallel using multiprocessing.

    This function runs `join_random_letters` and `add_random_numbers` in 
    four separate processes, each handling half of the workload. It measures 
    the total execution time and prints the duration in milliseconds.

    Parameters:
    n (int): The number of iterations, split among processes.

    Returns:
    float: The total execution time in milliseconds.
    """
    process_letters1 = multiprocessing.Process(target=join_random_letters, args=(n//2,))
    process_letters2 = multiprocessing.Process(target=join_random_letters, args=(n//2,))

    process_numbers1 = multiprocessing.Process(target=add_random_numbers, args=(n//2,))
    process_numbers2 = multiprocessing.Process(target=add_random_numbers, args=(n//2,))

    total_start_time = time.time()
    process_letters1.start()
    process_letters2.start()
    process_numbers1.start()
    process_numbers2.start()

    process_letters1.join()
    process_letters2.join()
    process_numbers1.join()
    process_numbers2.join()
    total_end_time = time.time()

    total_time = (total_end_time - total_start_time) * 1000
    print(f"Advanced Multiprocessing case taken: {total_time} milliseconds")
    return total_time